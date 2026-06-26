# Production-Ready Authentication API with CI/CD

## 📌 Project Overview

This project focuses on building a production-ready authentication and authorization API using modern backend engineering practices.

### Technology Stack

- FastAPI
- JWT Authentication
- Pytest
- GitHub Actions
- Docker
- CI/CD Pipeline

---

# Phase 1: Project Setup

## 🎯 Goal

Create a clean and runnable FastAPI project structure.

### Tasks

- Create project structure
- Set up virtual environment
- Install dependencies
- Run a basic FastAPI server

### Dependencies

```bash
pip install fastapi uvicorn pytest pytest-cov python-jose passlib[bcrypt]
```

### Basic Application

```python
# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}
```

### Run Application

```bash
uvicorn app.main:app --reload
```

---

# Phase 2: User Registration

## 🎯 Goal

Allow users to register securely.

### Tasks

- Define User model
- Hash passwords using bcrypt
- Create `/register` endpoint

### Authentication Flow

```text
function hash_password(password):
    return bcrypt.hash(password)

function register_user(email, password):
    if user_exists(email):
        raise error "User already exists"

    hashed = hash_password(password)

    save_user({
        email: email,
        password: hashed,
        role: "user"
    })

    return success
```

---

# Phase 3: Login & JWT Authentication

## 🎯 Goal

Authenticate users and issue JWT access tokens.

### Tasks

- Validate credentials
- Generate JWT tokens
- Set token expiration

### Authentication Flow

```text
function login(email, password):
    user = find_user(email)

    if not verify_password(password, user.password):
        raise error "Invalid credentials"

    token = create_jwt({
        sub: user.id,
        role: user.role,
        exp: now + 15min
    })

    return token
```

---

# Phase 4: Protected Routes

## 🎯 Goal

Secure endpoints using JWT authentication.

### Tasks

- Create authentication dependency
- Decode JWT token
- Retrieve current user

### Authorization Flow

```text
function get_current_user(token):
    payload = decode_jwt(token)

    if expired(payload):
        raise error "Token expired"

    return get_user(payload.sub)
```

### Protected Endpoint

```python
@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return user
```

---

# Phase 5: Role-Based Access Control (RBAC)

## 🎯 Goal

Restrict resources based on user roles.

### Tasks

- Add user roles (`user`, `admin`)
- Implement role validation

### RBAC Logic

```text
function require_role(role):
    function wrapper(user):
        if user.role != role:
            raise error "Forbidden"
        return user
    return wrapper
```

### Admin Endpoint

```python
@app.get("/admin/users")
def get_users(user = Depends(require_role("admin"))):
    return list_users()
```

---

# Phase 6: Refresh Tokens

## 🎯 Goal

Maintain user sessions without requiring frequent logins.

### Tasks

- Generate refresh tokens
- Store refresh tokens
- Implement token rotation

### Refresh Flow

```text
function refresh_token(old_refresh_token):
    if not valid(old_refresh_token):
        raise error

    invalidate(old_refresh_token)

    new_access = create_access_token()
    new_refresh = create_refresh_token()

    store(new_refresh)

    return new_access, new_refresh
```

---

# Phase 7: Logout & Token Blacklisting

## 🎯 Goal

Invalidate user sessions securely.

### Tasks

- Implement token blacklist
- Check blacklist on every request

### Logout Flow

```text
function logout(token):
    blacklist.add(token)

function is_blacklisted(token):
    return token in blacklist
```

### Authentication Check

```text
if is_blacklisted(token):
    reject_request()
```

---

# Phase 8: Logging & Audit Trail

## 🎯 Goal

Track and monitor authentication-related events.

### Tasks

- Log successful logins
- Log failed logins
- Log token refresh operations
- Maintain audit records

### Example Events

```text
log_event("LOGIN_SUCCESS", user_id)
log_event("LOGIN_FAILED", email)
log_event("TOKEN_REFRESHED", user_id)
```

---

# Phase 9: Testing

## 🎯 Goal

Achieve at least 80% code coverage.

### Tasks

- Write unit tests
- Write integration tests
- Configure coverage reporting

### Sample Tests

```python
def test_register_success():
    response = client.post("/register", data)
    assert response.status_code == 200
```

```python
def test_login_fail():
    response = client.post("/login", wrong_password)
    assert response.status_code == 401
```

### Coverage Command

```bash
pytest --cov=app --cov-fail-under=80
```

---

# Phase 10: Dockerization

## 🎯 Goal

Containerize the application.

### Tasks

- Create Dockerfile
- Create .dockerignore
- Build Docker image
- Run container locally

---

# Phase 11: Continuous Integration (CI)

## 🎯 Goal

Automate testing and validation.

### Tasks

- Configure GitHub Actions workflow
- Run automated tests
- Enforce coverage threshold
- Validate pull requests

---

# Phase 12: Build & Push Docker Image

## 🎯 Goal

Publish deployable application images.

### Tasks

- Authenticate with Docker Hub
- Build image automatically
- Push image to registry

---

# Phase 13: Automated Deployment

## 🎯 Goal

Deploy automatically to a virtual machine.

### Tasks

- Provision VM
- Install Docker
- Pull latest image
- Run updated container
- Configure deployment automation

---

# Phase 14: Slack Notifications

## 🎯 Goal

Receive deployment and pipeline alerts.

### Tasks

- Configure Slack webhook
- Send failure notifications
- Send deployment status updates

---

# System Workflow

```text
Write Code
    ↓
Run Tests Locally
    ↓
Dockerize Application
    ↓
Push to GitHub
    ↓
GitHub Actions Executes
    ↓
Run Tests & Coverage
    ↓
Build Docker Image
    ↓
Push to Docker Hub
    ↓
Deploy to Virtual Machine
    ↓
Send Slack Notifications
```

---

# Expected Deliverables

- Secure Authentication API
- JWT Access & Refresh Tokens
- Role-Based Access Control (RBAC)
- Token Blacklisting
- Audit Logging
- Automated Testing Suite
- Dockerized Application
- GitHub Actions CI Pipeline
- Automated Deployment Pipeline
- Slack Monitoring & Alerts

## Success Criteria

- Authentication system fully functional
- Protected routes secured
- RBAC enforced
- Test coverage ≥ 80%
- CI/CD pipeline operational
- Automated deployment working
- Production-ready Docker image available