# Makefile

.PHONY: setup-dev install-dev install-prod compile-dev compile-prod test run docker-build docker-run docker-stop docker-remove docker-restart docker-clean

# Default target to setup everything for development
run-dev: compile-dev install-dev test

# Compile production dependencies
compile-prod:
	pip-compile requirements.in

# Compile development dependencies
compile-dev: compile-prod
	pip-compile requirements-dev.in -o requirements-dev.txt

# Install production dependencies
install-prod:
	pip-sync requirements.txt

# Install development dependencies
install-dev: install-prod
	pip-sync requirements-dev.txt

# Run tests
test:
	python -m pytest

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
