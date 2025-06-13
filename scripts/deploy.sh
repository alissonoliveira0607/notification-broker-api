set -e

echo "🚀 Deploying Notification Broker API..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Load environment variables
source .env

# Build and deploy
echo "📦 Building Docker images..."
docker-compose build

echo "🔄 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Health check
echo "🏥 Performing health check..."
curl -f http://localhost:${PORT}/api/v1/notifications/health || {
    echo "❌ Health check failed"
    docker-compose logs notification-api
    exit 1
}

echo "✅ Deployment successful!"
echo "📡 API available at: http://localhost:${PORT}"
echo "🔍 Health check: http://localhost:${PORT}/api/v1/notifications/health"