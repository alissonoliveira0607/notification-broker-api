# src/main.py
from app_factory import create_app
from infrastructure.config.settings import Settings

settings = Settings.from_env()
app = create_app(settings)

# Isso aqui continua sendo útil apenas quando rodar via `python main.py`
if __name__ == "__main__":
    print(f"🚀 Notification Broker API starting...")
    print(f"📡 Server: http://{settings.HOST}:{settings.PORT}")
    print(f"🔐 API Key required in X-API-Key header")
    print(f"🏥 Health check: http://{settings.HOST}:{settings.PORT}/api/v1/notifications/health")
    
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )
