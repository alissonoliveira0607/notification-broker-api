import asyncio
import logging
from flask import Blueprint, request, jsonify
from typing import Dict, Any

from interface.middlewares.auth_middleware import require_api_key
from interface.serializers.notification_serializers import NotificationSerializer
from interface.exceptions.api_exceptions import APIException, ValidationException
from application.interfaces.notification_service import NotificationServiceInterface
from infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)

class NotificationController:
    
    def __init__(
        self,
        notification_service: NotificationServiceInterface,
        settings: Settings
    ):
        self.notification_service = notification_service
        self.settings = settings
        self.blueprint = self._create_blueprint()
    
    def _create_blueprint(self) -> Blueprint:
        """Create Flask blueprint with routes"""
        bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")
        
        @bp.route("/send", methods=["POST"])
        @require_api_key(self.settings)
        def send_notification():
            return asyncio.run(self._send_notification())
        
        @bp.route("/health", methods=["GET"])
        def health_check():
            return jsonify({"status": "healthy", "service": "notification-broker"})
        
        @bp.errorhandler(APIException)
        def handle_api_exception(e: APIException):
            return jsonify({"error": e.message}), e.status_code
        
        @bp.errorhandler(Exception)
        def handle_general_exception(e: Exception):
            logger.error(f"Unhandled exception: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
        
        return bp
    
    async def _send_notification(self) -> Dict[str, Any]:
        """Handle send notification request"""
        try:
            # Parse request data
            data = request.get_json()
            if not data:
                raise ValidationException("Request body is required")
            
            # Extract channel configs from headers
            headers = request.headers
            if headers.get("Slack-Webhook-Url"):
                data["slack_webhook_url"] = headers.get("Slack-Webhook-Url")
            if headers.get("Telegram-Bot-Token"):
                data["telegram_bot_token"] = headers.get("Telegram-Bot-Token")
            if headers.get("Telegram-Chat-Id"):
                data["telegram_chat_id"] = headers.get("Telegram-Chat-Id")
            
            # Deserialize and validate
            dto = NotificationSerializer.deserialize_send_request(data)
            
            # Send notification
            result = await self.notification_service.send_notification(dto)
            
            return jsonify({
                "success": True,
                "data": result
            }), 201
            
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Error processing notification request: {str(e)}")
            raise APIException(f"Failed to process notification: {str(e)}")