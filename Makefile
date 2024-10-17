# Makefile

.PHONY: run-dev install-dev install-prod compile-dev compile-prod test run docker-build docker-run docker-stop docker-remove docker-restart docker-clean init pre-commit lint format pre-commit-all

# Initialize the environment by installing pip-tools
init:
	pip install pip-tools

# Compile production dependencies
compile-prod: init
	pip-compile requirements.in

# Compile development dependencies
compile-dev: compile-prod
	pip-compile requirements-dev.in -o requirements-dev.txt

# Install production dependencies
install-prod: compile-prod
	pip-sync requirements.txt

# Install development dependencies
install-dev: install-prod compile-dev
	pip-sync requirements-dev.txt

# Install pre-commit hooks
pre-commit: install-dev
	pre-commit install

# Format code using Black
format:
	black app/ tests/

# Lint code using Flake8
lint:
	flake8 app/ tests/

# Run tests
test:
	python -m pytest

# Run all pre-commit checks including tests
pre-commit-all: install-dev
	pre-commit run --all-files

# Default target to setup everything for development and run tests
run-dev: install-dev pre-commit-all

# Run the application locally
run:
	uvicorn app.main:app --reload

# Build the Docker image
docker-build: compile-prod
	docker build -t agile-health-check-api .

# Stop the Docker container if it's running
docker-stop:
	docker stop agile-health-check-api || true

# Remove the Docker container if it exists
docker-remove:
	docker rm agile-health-check-api || true

# Run the Docker container with a specific name
docker-run: docker-stop docker-remove
	docker run -d -p 80:80 --name agile-health-check-api agile-health-check-api

# Rebuild the image and restart the container
docker-restart: docker-build docker-run

# Remove dangling images
docker-clean:
	docker image prune -f
