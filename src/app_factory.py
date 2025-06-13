import logging
from flask import Flask
from flask_cors import CORS

from infrastructure.config.settings import Settings
from infrastructure.repositories.in_memory_notification_repository import InMemoryNotificationRepository
from infrastructure.external_services.slack_service import SlackNotificationChannel
from infrastructure.external_services.telegram_service import TelegramNotificationChannel
from application.use_cases.send_notification import SendNotificationUseCase
from interface.controllers.notification_controller import NotificationController

def create_app(settings: Settings = None) -> Flask:
    """Application factory"""
    if settings is None:
        settings = Settings.from_env()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create Flask app
    app = Flask(__name__)
    app.config["DEBUG"] = settings.DEBUG
    
    # Enable CORS
    CORS(app)
    
    # Initialize dependencies
    notification_repository = InMemoryNotificationRepository()
    slack_channel = SlackNotificationChannel()
    telegram_channel = TelegramNotificationChannel()
    
    notification_service = SendNotificationUseCase(
        notification_repository=notification_repository,
        slack_channel=slack_channel,
        telegram_channel=telegram_channel
    )
    
    # Create controllers
    notification_controller = NotificationController(
        notification_service=notification_service,
        settings=settings
    )
    
    # Register blueprints
    app.register_blueprint(notification_controller.blueprint)
    
    return app