from fastapi import FastAPI
from aiosmtpd.controller import Controller

from logs import Logger

logger = Logger().logger


class CustomMessageHandler:

    async def handle_DATA(self, server, session, envelope):
        logger.info(f"Message received: {envelope.mail_from} -> {envelope.rcpt_tos}")
        return "250 Message accepted for delivery"


def app_lifespan():
    handler = CustomMessageHandler()
    controller = Controller(handler, hostname="127.0.0.1", port=8025)

    async def lifespan(app: FastAPI):
        controller.start()
        logger.info("SMTP server started")
        yield
        controller.stop()
        logger.info("SMTP server stopped")

    return lifespan
