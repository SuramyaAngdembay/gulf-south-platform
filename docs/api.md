# API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication

All API endpoints except login and registration require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### POST /auth/login
Login with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### POST /auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false
}
```

### Users

#### GET /users/me
Get current user information.

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-03-21T13:00:00"
}
```

#### PUT /users/me
Update current user information.

**Request Body:**
```json
{
  "full_name": "John Smith"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Smith",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-03-21T13:00:00"
}
```

### Messages

#### GET /messages/conversations
Get all conversations for the current user.

**Response:**
```json
[
  {
    "id": 1,
    "user1_id": 1,
    "user2_id": 2,
    "updated_at": "2024-03-21T13:00:00",
    "last_message": {
      "content": "Hello!",
      "created_at": "2024-03-21T13:00:00"
    }
  }
]
```

#### GET /messages/conversations/{conversation_id}
Get messages in a specific conversation.

**Response:**
```json
[
  {
    "id": 1,
    "conversation_id": 1,
    "sender_id": 1,
    "content": "Hello!",
    "read": true,
    "created_at": "2024-03-21T13:00:00"
  }
]
```

#### POST /messages/conversations/{conversation_id}
Send a message in a conversation.

**Request Body:**
```json
{
  "content": "Hello!"
}
```

**Response:**
```json
{
  "id": 1,
  "conversation_id": 1,
  "sender_id": 1,
  "content": "Hello!",
  "read": false,
  "created_at": "2024-03-21T13:00:00"
}
```

### Notifications

#### GET /notifications
Get all notifications for the current user.

**Response:**
```json
[
  {
    "id": 1,
    "type": "message",
    "message": "New message from John Doe",
    "data": {
      "conversation_id": 1,
      "sender_id": 2
    },
    "read": false,
    "created_at": "2024-03-21T13:00:00"
  }
]
```

#### PUT /notifications/{notification_id}/read
Mark a notification as read.

**Response:**
```json
{
  "id": 1,
  "type": "message",
  "message": "New message from John Doe",
  "data": {
    "conversation_id": 1,
    "sender_id": 2
  },
  "read": true,
  "created_at": "2024-03-21T13:00:00"
}
```

## WebSocket Endpoints

### ws://localhost:5000/ws
WebSocket connection for real-time messaging and notifications.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:5000/ws');
ws.onopen = () => {
  // Send authentication token
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'your_jwt_token'
  }));
};
```

**Message Format:**
```json
{
  "type": "message",
  "data": {
    "conversation_id": 1,
    "sender_id": 2,
    "content": "Hello!",
    "created_at": "2024-03-21T13:00:00"
  }
}
```

**Notification Format:**
```json
{
  "type": "notification",
  "data": {
    "id": 1,
    "type": "message",
    "message": "New message from John Doe",
    "data": {
      "conversation_id": 1,
      "sender_id": 2
    }
  }
}
``` 