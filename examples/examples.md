# API Endpoints Examples

## User Endpoints

### Get user by ID
```
GET /user/{user_id}
```

### Example curl command
```
curl -X GET "http://localhost:8000/user/1"
```

### Get all users
```
GET /users
```

### Example curl command
```
curl -X GET "http://localhost:8000/users"
```

### Create a new user
```
POST /user
Content-Type: application/json

{
  "user_name": "John Doe"
}
```

### Example curl command
```
curl -X POST "http://localhost:8000/user" \
  -H "Content-Type: application/json" \
  -d '{"user_name": "John Doe"}'
```

## Device Endpoints

### Get device by ID
```
GET /device/{device_id}
```

### Example curl command
```
curl -X GET "http://localhost:8000/device/1"
```

### Get devices for a user
```
GET /user/{user_id}/devices
```

### Example curl command
```
curl -X GET "http://localhost:8000/user/1/devices"
```

### Create a new device for a user
```
POST /user/{user_id}/device
Content-Type: application/json

{
  "device_name": "iPhone 14"
}
```

### Example curl command
```
curl -X POST "http://localhost:8000/user/1/device" \
  -H "Content-Type: application/json" \
  -d '{"device_name": "iPhone 14"}'
```

## Message Endpoints

### Get all messages for a device
```
GET /device/{device_id}/messages
```

### Example curl command
```
curl -X GET "http://localhost:8000/device/1/messages"
```

### Get messages within a date range
```
GET /device/{device_id}/messages?startDate=2023-01-01&endDate=2023-12-31
```

### Example curl command
```
curl -X GET "http://localhost:8000/device/1/messages?startDate=2023-01-01&endDate=2023-12-31"
```

### Get messages within a date range with specific guid
```
GET /device/{device_id}/messages?startDate=2023-01-01&endDate=2023-12-31&guid=example-guid
```

### Create a new message
```
POST /device/{device_id}/message
Content-Type: application/json

{
  "guid": "message-guid-123",
  "conversation_guid": "conv-guid-123",
  "conversation_conversation": "Conversation Name",
  "conversation_display_name": "Display Name",
  "date": "2023-01-15T10:30:00",
  "sender_full_name": "John Doe",
  "sender_phone_numbers": "+1234567890",
  "type": "sms",
  "body": "Hello, this is a test message"
}
```

### Example curl command
```
curl -X POST "http://localhost:8000/device/1/message" \
  -H "Content-Type: application/json" \
  -d '{"guid": "message-guid-123", "conversation_guid": "conv-guid-123", "conversation_conversation": "Conversation Name", "conversation_display_name": "Display Name", "date": "2023-01-15T10:30:00", "sender_full_name": "John Doe", "sender_phone_numbers": "+1234567890", "type": "sms", "body": "Hello, this is a test message"}'
```

## HealthData Endpoints

### Get all health data for a device
```
GET /device/{device_id}/health
```

### Example curl command
```
curl -X GET "http://localhost:8000/device/1/health"
```

### Get health data within a date range
```
GET /device/{device_id}/health?startDate=2023-01-01&endDate=2023-12-31
```

### Example curl command
```
curl -X GET "http://localhost:8000/device/1/health?startDate=2023-01-01&endDate=2023-12-31"
```

### Get health data within a date range with specific guid
```
GET /device/{device_id}/health?startDate=2023-01-01&endDate=2023-12-31&guid=example-guid
```

### Create new health data
```
POST /device/{device_id}/health
Content-Type: application/json

{
  "name": "Heart Rate",
  "source": "Apple Watch",
  "duration": "1 hour",
  "startdate": "2023-01-15T10:00:00",
  "enddate": "2023-01-15T11:00:00",
  "unit": "bpm",
  "value": "72",
  "type": "heart_rate"
}
```

### Example curl command
```
curl -X POST "http://localhost:8000/device/1/health" \
  -H "Content-Type: application/json" \
  -d '{"name": "Heart Rate", "source": "Apple Watch", "duration": "1 hour", "startdate": "2023-01-15T10:00:00", "enddate": "2023-01-15T11:00:00", "unit": "bpm", "value": "72", "type": "heart_rate"}'
```

## ScreenTime Endpoints

### Get all screen time for a device
```
GET /device/{device_id}/screen-time
```

### Example curl command
```
curl -X GET "http://localhost:8000/device/1/screen-time"
```

### Get screen time within a date range
```
GET /device/{device_id}/screen-time?startDate=2023-01-01&endDate=2023-12-31
```

### Example curl command
```
curl -X GET "http://localhost:8000/device/1/screen-time?startDate=2023-01-01&endDate=2023-12-31"
```

### Get screen time within a date range for a specific app
```
GET /device/{device_id}/screen-time?startDate=2023-01-01&endDate=2023-12-31&app=example-app
```

### Create new screen time
```
POST /device/{device_id}/screen-time
Content-Type: application/json

{
  "app": "com.apple.mobilesafari",
  "website": "https://www.example.com",
  "duration": "30 minutes",
  "description": "Web browsing session",
  "activity_date": "2023-01-15"
}
```

### Example curl command
```
curl -X POST "http://localhost:8000/device/1/screen-time" \
  -H "Content-Type: application/json" \
  -d '{"app": "com.apple.mobilesafari", "website": "https://www.example.com", "duration": "30 minutes", "description": "Web browsing session", "activity_date": "2023-01-15"}'
```

## Testing Instructions

1. Start the server: `python main.py`
2. Use curl or any HTTP client to test the endpoints
3. Replace `{device_id}` with an actual device ID from your database
4. Replace date values with valid date ranges in YYYY-MM-DD format
5. For endpoints that support additional parameters, include them in the query string
6. All date parameters should be in YYYY-MM-DD format
7. For POST requests, make sure to include the appropriate JSON body