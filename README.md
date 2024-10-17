# Agile Team Health Check API

![Build Status](https://github.com/peiman/agile-team-health-check-api/actions/workflows/ci.yml/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An API for measuring and visualizing the health of Agile teams using survey instruments.

## Table of Contents

- [Agile Team Health Check API](#agile-team-health-check-api)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [API Documentation](#api-documentation)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Usage](#usage)
    - [Running Locally](#running-locally)
    - [Using Docker](#using-docker)
  - [Available Surveys](#available-surveys)
  - [Development](#development)
    - [Running Tests](#running-tests)
    - [Code Quality](#code-quality)
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
- **Code Quality** checks with black, flake8, mypy, and bandit

## API Documentation

The API documentation is available once you run the application:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

These provide interactive interfaces to explore and test the API endpoints.

## Installation

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerization)
- Git (for version management)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agile-team-health-check-api.git
   cd agile-team-health-check-api
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Locally

To run the application locally:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Using Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Run the Docker container:
   ```bash
   docker-compose up
   ```

The API will be available at `http://localhost:8000`.

## Available Surveys

The API currently includes the following surveys:

1. **Subjective Happiness Scale (SHS)**
   - ID: 1
   - Type: Weekly
   - Questions: 4

2. **Single-Item Stress Measure**
   - ID: 2
   - Type: Weekly
   - Questions: 1

## Development

### Running Tests

To run the test suite:

```bash
pytest
```

### Code Quality

We use several tools to maintain code quality:

- **black**: For code formatting
- **flake8**: For style guide enforcement
- **mypy**: For static type checking
- **bandit**: For security linting

To run all code quality checks:

```bash
pre-commit run --all-files
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

Please ensure your code adheres to our coding standards and passes all tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Github: @peiman

Project Link: [https://github.com/yourusername/agile-team-health-check-api](https://github.com/yourusername/agile-team-health-check-api)
