__version__ = "0.1.0"

import os
import asyncio
import ssl

import aiohttp
import string
import random
import json
from uuid import uuid4
from datetime import datetime, timedelta
from email.message import EmailMessage

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from logs import Logger

from schemas import URLParams
from schemas import Office

# Load environment variables
load_dotenv()


class App:

    def __init__(self):
        self.logger = Logger().logger
        self.version = __version__
        self.secret_key = os.getenv("SECRET_KEY")
        self.fernet = Fernet(self.secret_key)
        self.queue = {}
        self.tasks = {}
        self.ssl_context = self.set_ssl_context()
        self.endpoint = (
            "https://citaprevia-sede.sepe.gob.es/citapreviasepe/cita/cargaOficinasMapa"
        )
        with open(os.path.join(os.getenv("DATA_PATH"), "postal.json"), "r") as f:
            self.postal = json.loads(f.read())
        asyncio.create_task(self.expire_queue())
        self.logger.info(f"App started - v{__version__}")

    @staticmethod
    def set_ssl_context():
        """
        Sets the SSL context for the HTTP requests.
        """
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    async def expire_queue(self):
        """
        Expires the queue every minute.
        """
        while True:
            expired_ids = [
                _id
                for _id, payload in self.queue.items()
                if payload["expires"] < datetime.now()
            ]
            for random_id in expired_ids:
                self.queue.pop(random_id)
                self.logger.info(f"Queue id {random_id} - Expired")
            await asyncio.sleep(60)

    async def send_request(self, postal_code):
        """
        Sends a request to the given endpoint every 10 seconds.
        Each instance of this coroutine handles its own timing.
        """
        task_id = self.tasks[postal_code]["task_id"]
        lat = str(self.postal[postal_code]["latitud"])
        lng = str(self.postal[postal_code]["longitud"])
        url_params = URLParams(
            codigoPostal=postal_code,
            latOrigen=lat,
            lngOrigen=lng,
        ).model_dump()

        while postal_code in self.tasks:
            subscribers = self.tasks[postal_code]["subscribers"]
            expiration_date = sorted(subscribers, key=lambda x: x["expires"])[-1].get(
                "expires"
            )
            expires = (expiration_date - datetime.now()).seconds
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(
                        self.endpoint, data=url_params, ssl=self.ssl_context
                    )
                    offices = await self.process_response(await response.json())
                    self.logger.info(
                        f"Task {task_id} - Expires In: {expires} - Postal {postal_code} - "
                        f"Subscribers {len(subscribers)} - Available Offices: {len(offices)}"
                    )
                    if offices:
                        await self.send_email(
                            subscribers=subscribers,
                            offices=offices,
                            postal_code=postal_code,
                        )
            except Exception as e:
                self.logger.error(f"Task {task_id}: Error: {e}")

            for _ in range(20):
                subscribers = self.tasks[postal_code]["subscribers"]
                if not subscribers:
                    self.tasks[postal_code]["task"].cancel()
                    self.tasks.pop(postal_code)
                    self.logger.info(
                        f"Task {task_id} - Postal {postal_code} - Finished"
                    )
                    break
                for subscriber in subscribers:
                    if subscriber["expires"] < datetime.now():
                        await self.remove_subscription(subscriber["token"])
                await asyncio.sleep(1)

    @staticmethod
    async def process_response(response: dict):
        """
        Processes the response from the endpoint.
        """
        available_offices = []
        for office in response.get("listaOficina", []):
            if office.get("primerHuecoDisponible", False):
                available_offices.append(Office(**office))
        return available_offices

    async def send_email(self, subscribers: list, offices: list, postal_code: str):
        """
        Sends an email to the subscribers with the available offices.
        """

        msg = EmailMessage()
        msg.set_content(json.dumps([office.dict() for office in offices], indent=4))
        msg["Subject"] = f"Alert - {datetime.now()} - {len(offices)} offices available"
        msg["From"] = "xabi.moreno.maya@gmail.com"
        msg["To"] = ";".join([subscriber["user_email"] for subscriber in subscribers])

        self.logger.info(
            f"Email alert sent to {len(subscribers)} subscribers - Postal {postal_code}"
        )
        self.logger.debug(f"Message: {msg.get_content()}")

    async def decrypt_token(self, token: str):
        """
        Decrypts a token.
        """
        try:
            payload = json.loads(self.fernet.decrypt(token.encode()).decode())
            subscription_id = payload["id"]
            postal_code = payload["postal_code"]
            user_email = payload["user_email"]
        except Exception as e:
            self.logger.error(f"Token Error: {type(e).__name__} {e}")
            raise HTTPException(status_code=400, detail="Invalid token")
        return subscription_id, postal_code, user_email

    async def queue_subscription(self, postal_code: str, user_email: str):
        """
        Queues a user to subscribe to a task.
        """
        postal_code = await self.validate_postal_code(postal_code)

        if (
            postal_code in self.tasks
            and user_email in self.tasks[postal_code]["subscribers"]
        ):
            self.logger.warning(
                f"User {user_email} is already subscribed to postal_code {postal_code}"
            )
            raise HTTPException(
                status_code=400, detail=f"User {user_email} is already subscribed"
            )

        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        payload = {
            "id": random_id,
            "postal_code": postal_code,
            "user_email": user_email,
        }
        validation_token = self.fernet.encrypt(json.dumps(payload).encode()).decode()
        self.queue[random_id] = {
            **payload,
            "expires": datetime.now() + timedelta(minutes=5),
        }
        self.logger.info(
            f"User {user_email} queued to subscribe to postal_code {postal_code}"
        )
        return JSONResponse(
            status_code=200,
            content={
                "detail": f"User {user_email} queued to subscribe to postal_code {postal_code}",
                "validation_token": validation_token,
            },
        )

    async def validate_subscription(self, token: str):
        """
        Validates a user subscription.
        """
        subscription_id, postal_code, user_email = await self.decrypt_token(token)
        if subscription_id not in self.queue:
            detail = f"User {user_email} not queued to subscribe to postal_code {postal_code}"
            self.logger.warning(detail)
            raise HTTPException(status_code=404, detail=detail)

        self.queue.pop(subscription_id)
        await self.subscribe(
            postal_code=postal_code, user_email=user_email, token=token
        )
        return JSONResponse(
            status_code=200,
            content={
                "detail": f"User {user_email} subscribed to postal_code {postal_code}"
            },
        )

    async def subscribe(self, postal_code: str, user_email: str, token: str):
        """
        Subscribes a user to an existing task.
        """
        postal_code = await self.validate_postal_code(postal_code)
        if postal_code not in self.tasks:
            await self.create_task(postal_code=postal_code)

        subscribers = {
            user["user_email"] for user in self.tasks[postal_code]["subscribers"]
        }
        if user_email in subscribers:
            self.logger.warning(
                f"User {user_email} is already subscribed to postal_code {postal_code}"
            )
            raise HTTPException(
                status_code=400, detail=f"User {user_email} is already subscribed"
            )

        expiration = datetime.now() + timedelta(hours=24)
        subscriber = {"user_email": user_email, "expires": expiration, "token": token}
        self.tasks[postal_code]["subscribers"].append(subscriber)
        self.logger.info(
            f"User {user_email} subscribed to postal_code {postal_code} - Expires {expiration.isoformat()}"
        )
        return JSONResponse(
            status_code=200,
            content={
                "detail": f"User {user_email} subscribed to postal_code {postal_code}"
            },
        )

    async def remove_subscription(self, token: str):
        """
        Removes a user subscription.
        """
        subscription_id, postal_code, user_email = await self.decrypt_token(token)
        postal_code = await self.validate_postal_code(postal_code)
        subscribers = {
            user["user_email"] for user in self.tasks[postal_code]["subscribers"]
        }
        if postal_code not in self.tasks or user_email not in subscribers:
            self.logger.warning(
                f"User {user_email} is not subscribed to postal_code {postal_code}"
            )
            raise HTTPException(
                status_code=404,
                detail=f"User {user_email} is not subscribed to postal_code {postal_code}",
            )

        self.tasks[postal_code]["subscribers"] = [
            subscriber
            for subscriber in self.tasks[postal_code]["subscribers"]
            if subscriber.get("user_email") != user_email
        ]
        self.logger.info(
            f"User {user_email} unsubscribed from postal_code {postal_code}"
        )
        return JSONResponse(
            status_code=200,
            content={
                "detail": f"User {user_email} unsubscribed from postal_code {postal_code}"
            },
        )

    async def create_task(self, postal_code: str):
        """
        Creates a new task for the given postal code.
        """
        task = {
            "task_id": str(uuid4()),
            "task": asyncio.create_task(self.send_request(postal_code=postal_code)),
            "subscribers": [],
        }
        self.tasks[postal_code] = task
        self.logger.info(f"Task {task['task_id']} - Postal {postal_code} - Started")

    async def validate_postal_code(self, postal_code: str):
        """
        Validates the postal code.
        """
        if postal_code not in self.postal:
            self.logger.warning(f"Postal code {postal_code} not found")
            raise HTTPException(
                status_code=404, detail=f"Postal code {postal_code} not found"
            )
        return postal_code
