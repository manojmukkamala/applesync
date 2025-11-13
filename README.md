# Apple-Sync API

A FastAPI-based API for syncing Apple device data.

## Features

- User management
- Device management
- Message synchronization
- Health data synchronization
- JWT-based authentication

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (see .env.example)
4. Run the application:
   ```bash
   python main.py
   ```

## API Endpoints

### Authentication
- `POST /login` - Authenticate user and get access token

### Users
- `GET /user/{user_id}` - Get user by ID
- `GET /users` - Get all users
- `POST /user` - Create new user

### Devices
- `GET /device/{device_id}` - Get device by ID
- `GET /user/{user_id}/devices` - Get devices for user
- `POST /user/{user_id}/device` - Create device for user

### Messages
- `GET /message/{guid}` - Get message by GUID
- `GET /device/{device_id}/messages` - Get messages for device

### Health Data
- `GET /health/{health_id}` - Get health data by ID
- `GET /device/{device_id}/health` - Get health data for device
- `POST /device/{device_id}/health` - Create health data for device

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-super-secret-key-here-change-this-in-production
```

## Authentication

All endpoints except `/login` require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_token_here>
```

## Database

The application uses SQLite with SQLModel for database operations.


Testing Authorization:

1. Initialize DB and create a user
```bash
python -m scripts.utils create-user --username admin --password secret_password
```

2. [optional- I have already put the scret in .env file] Run the API
```bash
export SECRET_KEY="$(python - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
)"
uvicorn app.routes:app --reload --port 8000
```

Get a token (login)
```bash
curl -s -X POST "http://127.0.0.1:8000/login" \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=admin&password=secret_password"
```

Call protected endpoints with the token
```bash
TOKEN="<paste_access_token_here>"
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/users
```

