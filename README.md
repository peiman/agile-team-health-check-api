# Agile Team Health Check API

![Build Status](https://github.com/peiman/agile-team-health-check-api/actions/workflows/ci.yml/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An API for measuring and visualizing the health of Agile teams using survey instruments.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
  - [Makefile Commands](#makefile-commands)
  - [Running Locally](#running-locally)
  - [Using Docker](#using-docker)
- [Available Surveys](#available-surveys)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The Agile Team Health Check API provides endpoints to conduct surveys, calculate scores, and help Agile teams assess their well-being and performance. It includes built-in surveys like the Subjective Happiness Scale (SHS) and the Single-Item Stress Measure.

## Features

- **RESTful API** built with FastAPI
- **Interactive Documentation** with Swagger UI and ReDoc
- **Modular Design** with support for adding new surveys
- **Automated Testing** using pytest
- **Error Handling** and **Logging**
- **Flexible Survey Management** with a `SurveyRegistry` class
- **Dependency Management** using pip-tools
- **Docker Support** for containerization

## API Documentation

The API documentation is available once you run the application:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

These provide interactive interfaces to explore and test the API endpoints.

## Installation

### Prerequisites

- **Python 3.7 or higher**
- **pip**
- **Make**
- **Docker** (optional, for containerization)

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/agile-team-health-check-api.git
   cd agile-team-health-check-api
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Development Dependencies**

   ```bash
   make install-dev
   ```

   This command will:

   - Compile production dependencies using `pip-compile requirements.in`
   - Compile development dependencies using `pip-compile requirements-dev.in -o requirements-dev.txt`
   - Sync production dependencies using `pip-sync requirements.txt`
   - Sync development dependencies using `pip-sync requirements-dev.txt`

## Usage

### Makefile Commands

The `Makefile` provides a set of commands to manage your project efficiently. Here's a breakdown of the available commands:

- **`make run-dev`**: Compiles development dependencies, installs them, and runs tests.

  ```bash
  make run-dev
  ```

- **`make compile-prod`**: Compiles production dependencies.

  ```bash
  make compile-prod
  ```

- **`make compile-dev`**: Compiles both production and development dependencies.

  ```bash
  make compile-dev
  ```

- **`make install-prod`**: Installs production dependencies.

  ```bash
  make install-prod
  ```

- **`make install-dev`**: Installs both production and development dependencies.

  ```bash
  make install-dev
  ```

- **`make test`**: Runs the test suite using pytest.

  ```bash
  make test
  ```

- **`make run`**: Runs the application locally using Uvicorn.

  ```bash
  make run
  ```

- **`make docker-build`**: Builds the Docker image for the application.

  ```bash
  make docker-build
  ```

- **`make docker-run`**: Runs the Docker container.

  ```bash
  make docker-run
  ```

- **`make docker-stop`**: Stops the running Docker container.

  ```bash
  make docker-stop
  ```

- **`make docker-remove`**: Removes the Docker container.

  ```bash
  make docker-remove
  ```

- **`make docker-restart`**: Rebuilds and restarts the Docker container.

  ```bash
  make docker-restart
  ```

- **`make docker-clean`**: Removes dangling Docker images.

  ```bash
  make docker-clean
  ```

### Running Locally

To run the application locally, use the `make run` command:

```bash
make run
```

This will start the FastAPI server with hot-reloading enabled. Access the API at [http://localhost:8000](http://localhost:8000).

### Using Docker

1. **Build the Docker Image**

   ```bash
   make docker-build
   ```

2. **Run the Docker Container**

   ```bash
   make docker-run
   ```

   This will start the container in detached mode, mapping port `80` of the container to port `80` on your host.

3. **Stop the Docker Container**

   ```bash
   make docker-stop
   ```

4. **Remove the Docker Container**

   ```bash
   make docker-remove
   ```

5. **Rebuild and Restart the Docker Container**

   ```bash
   make docker-restart
   ```

6. **Clean Up Dangling Images**

   ```bash
   make docker-clean
   ```

## Available Surveys

The API currently includes the following surveys:

1. **Subjective Happiness Scale (SHS)**
   - **ID**: 1
   - **Type**: Weekly
   - **Questions**: 4

2. **Single-Item Stress Measure**
   - **ID**: 2
   - **Type**: Weekly
   - **Questions**: 1

### Listing All Surveys

Retrieve a list of all available surveys:

```bash
GET http://localhost:8000/surveys/
```

### Getting Survey Details

Retrieve detailed information about a specific survey, including its questions:

```bash
GET http://localhost:8000/surveys/{survey_id}
```

Replace `{survey_id}` with the actual survey ID (e.g., `1` or `2`).

### Submitting Survey Responses

Submit responses to a survey to receive a calculated assessment result:

```bash
POST http://localhost:8000/surveys/{survey_id}/responses
```

**Payload Example:**

```json
{
  "survey_id": 1,
  "answers": [
    {"question_id": 1, "score": 5},
    {"question_id": 2, "score": 6},
    {"question_id": 3, "score": 3},
    {"question_id": 4, "score": 2}
  ],
  "timestamp": "2023-10-14T12:00:00Z"
}
```

## Running Tests

Ensure all tests pass to verify the integrity of the application:

```bash
make test
```

Or directly with:

```bash
python -m pytest
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes and Commit**

   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**

   Open a pull request on the main repository with a description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).
