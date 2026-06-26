# Authentication API with CI/CD

A production-ready Authentication and Authorization API built using modern backend engineering practices.

## Features

- **FastAPI Framework**: High-performance asynchronous API routing.
- **JWT Authentication**: Secure login with short-lived access tokens and long-lived refresh tokens.
- **Role-Based Access Control (RBAC)**: Differentiate access between standard users and administrators.
- **Security**: Password hashing with `bcrypt` and token blacklisting for secure logouts.
- **Testing**: Comprehensive test suite using `pytest` with 80%+ coverage enforced.
- **CI/CD**: Fully automated testing pipeline using GitHub Actions and containerization via Docker.

## Technology Stack

- **Backend**: Python 3.10, FastAPI, SQLAlchemy, Pydantic
- **Security**: python-jose (JWT), passlib (bcrypt)
- **Testing**: pytest, pytest-cov
- **DevOps**: Docker, GitHub Actions

## Getting Started (Local Development)

### 1. Clone & Setup
Clone the repository and set up your virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the development server:
```bash
uvicorn app.main:app --reload
```
You can now access the interactive API documentation at: `http://127.0.0.1:8000/docs`

## Testing

Run the test suite with coverage reporting:
```bash
pytest --cov=app --cov-fail-under=80
```

## Docker Deployment

To build and run the application using Docker:

1. **Build the image**:
```bash
docker build -t auth-api .
```

2. **Run the container**:
```bash
docker run -d -p 8000:8000 --name auth-api-container auth-api
```
The API will be available at `http://localhost:8000`.

## Continuous Integration

This project uses **GitHub Actions**. Any push or Pull Request to the `main` branch will automatically trigger a pipeline that:
1. Sets up Python 3.10
2. Installs all required dependencies
3. Runs the full test suite and enforces an 80% minimum code coverage.
