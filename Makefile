.PHONY: build run test clean dev-up dev-down prod-up prod-down

# Docker commands
build:
	docker-compose build

run:
	docker-compose up

run-detached:
	docker-compose up -d

stop:
	docker-compose down

# Development
dev-up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

dev-down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

# Production
prod-up:
	docker-compose up -d

prod-down:
	docker-compose down


# Code quality
lint:
	docker-compose exec notification-api flake8 src/
	docker-compose exec notification-api mypy src/

format:
	docker-compose exec notification-api black src/ tests/

security-check:
	docker-compose exec notification-api bandit -r src/

# Logs
logs:
	docker-compose logs -f notification-api

# Clean up
clean:
	docker-compose down -v
	docker system prune -f

# Setup development environment
setup-dev:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install