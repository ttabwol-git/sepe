import sys
import os

from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

os.environ["ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_PATH"] = os.path.join(os.environ["ROOT_PATH"], "src")
os.environ["DATA_PATH"] = os.path.join(os.environ["ROOT_PATH"], "data")
sys.path.insert(0, os.environ["SRC_PATH"])
sys.path.insert(1, os.environ["DATA_PATH"])

from app import App
from logs import Logger
from schemas import Task
from smtp import app_lifespan


class API:

    def __init__(self):
        self.app = App()
        self.version = self.app.version
        self.logger = Logger().logger
        self.api = FastAPI(lifespan=app_lifespan())
        self.logger.info(f"API started - v{self.version}")
        self.routers()
        self.add_cors_middleware()

    def add_cors_middleware(self):
        """Adds CORS middleware to the FastAPI application"""
        self.api.add_middleware(
            CORSMiddleware,  # type: ignore
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def routers(self):

        @self.api.get("/postal")
        def get_postal():
            self.logger.info("Retrieving postal codes")
            response = []
            for key in sorted(self.app.postal.keys()):
                response.append({"code": key})
            return response

        @self.api.post("/subscription/queue")
        async def queue_subscription(task: Task):
            self.logger.info(f"Queueing {task.user_email} to {task.postal_code}")
            return await self.app.queue_subscription(
                postal_code=task.postal_code, user_email=task.user_email
            )

        @self.api.get("/subscription/validate")
        async def validate_subscription(token: str = Query()):
            self.logger.info(f"Validating subscription from token {token[:5]}...")
            return await self.app.validate_subscription(token=token)

        @self.api.get("/subscription/remove")
        async def remove_subscription(token: str = Query()):
            self.logger.info(f"Removing subscription from token {token[:5]}...")
            return await self.app.remove_subscription(token=token)


api = API().api

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="critical")
