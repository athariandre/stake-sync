# API Documentation

## Base URL

Local: `http://localhost:8000`
Production: `https://yourdomain.com`

## Interactive Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Authentication

The MVP does not require authentication for most endpoints. User ID is passed as a parameter.

**Note:** In production, implement proper authentication using JWT tokens.

## Endpoints

### Health & Status

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### User Management

#### POST /auth/register

Register a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

#### GET /auth/user/{user_id}

Get user details.

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

### Weekly Updates

#### POST /update/submit

Submit a new weekly update.

**Request Body:**
```json
{
  "user_id": 1,
  "content": "This week we achieved X, Y, and Z. Key challenges were A and B. Next week we plan to focus on C."
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "content": "This week we achieved...",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### GET /update/list

List all updates for a user.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "content": "This week we achieved...",
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

#### GET /update/{update_id}

Get a specific update.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "content": "This week we achieved...",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

### Style Management

#### POST /style/upload

Upload a writing sample for style analysis.

**Request Body:**
```json
{
  "user_id": 1,
  "content": "Sample of your writing..."
}
```

**Response:**
```json
{
  "message": "Style sample uploaded successfully",
  "style_profile": {
    "tone": "professional and balanced",
    "sentence_length": "medium",
    "preferred_phrases": ["looking forward", "excited to"],
    "avoid_phrases": [],
    "audience_modifiers": {
      "investors": "upbeat and confident",
      "employees": "supportive and motivating",
      "partners": "honest and collaborative"
    }
  }
}
```

#### GET /style/profile

Get user's style profile.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "user_id": 1,
  "style_profile": {
    "tone": "professional and balanced",
    "sentence_length": "medium",
    "preferred_phrases": ["looking forward", "excited to"],
    "avoid_phrases": [],
    "audience_modifiers": {
      "investors": "upbeat and confident",
      "employees": "supportive and motivating",
      "partners": "honest and collaborative"
    }
  }
}
```

---

### Draft Generation

#### POST /drafts/generate/{update_id}

Generate drafts for all three audiences.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "investors": {
    "id": 1,
    "update_id": 1,
    "user_id": 1,
    "audience": "investors",
    "content": "Dear investors, this week we...",
    "status": "draft",
    "created_at": "2024-01-15T10:35:00",
    "updated_at": "2024-01-15T10:35:00"
  },
  "employees": {
    "id": 2,
    "update_id": 1,
    "user_id": 1,
    "audience": "employees",
    "content": "Team, this week we...",
    "status": "draft",
    "created_at": "2024-01-15T10:35:00",
    "updated_at": "2024-01-15T10:35:00"
  },
  "partners": {
    "id": 3,
    "update_id": 1,
    "user_id": 1,
    "audience": "partners",
    "content": "Partners, this week we...",
    "status": "draft",
    "created_at": "2024-01-15T10:35:00",
    "updated_at": "2024-01-15T10:35:00"
  }
}
```

#### GET /drafts/{draft_id}

Get a specific draft.

**Response:**
```json
{
  "id": 1,
  "update_id": 1,
  "user_id": 1,
  "audience": "investors",
  "content": "Dear investors, this week we...",
  "status": "draft",
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

---

### Review Workflow

#### POST /review/apply-edits/{draft_id}

Apply natural language edits to a draft.

**Request Body:**
```json
{
  "user_id": 1,
  "edit_instructions": "Make it more concise and add specific metrics"
}
```

**Response:**
```json
{
  "id": 1,
  "update_id": 1,
  "user_id": 1,
  "audience": "investors",
  "content": "Updated draft with edits...",
  "status": "edited",
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:40:00"
}
```

#### POST /review/manual-edit/{draft_id}

Manually edit a draft with new content.

**Request Body:**
```json
{
  "user_id": 1,
  "new_content": "Completely new draft content..."
}
```

**Response:**
```json
{
  "id": 1,
  "update_id": 1,
  "user_id": 1,
  "audience": "investors",
  "content": "Completely new draft content...",
  "status": "edited",
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:45:00"
}
```

#### POST /review/approve/{draft_id}

Approve a draft.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "id": 1,
  "update_id": 1,
  "user_id": 1,
  "audience": "investors",
  "content": "Draft content...",
  "status": "approved",
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:50:00"
}
```

#### POST /review/reject/{draft_id}

Reject a draft.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "id": 1,
  "update_id": 1,
  "user_id": 1,
  "audience": "investors",
  "content": "Draft content...",
  "status": "rejected",
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:55:00"
}
```

#### POST /review/regenerate/{draft_id}

Regenerate a draft from scratch.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "id": 1,
  "update_id": 1,
  "user_id": 1,
  "audience": "investors",
  "content": "Newly regenerated draft...",
  "status": "draft",
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

---

### Email Sending

#### POST /send/{draft_id}

Send an approved draft via email.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "draft_id": 1,
  "recipients_count": 5,
  "status": "sent",
  "sent_at": "2024-01-15T11:05:00"
}
```

**Errors:**
- 400: Draft not approved
- 404: No recipients configured for this audience

---

### Audience Management

#### POST /audience/create

Create or update an audience group.

**Request Body:**
```json
{
  "user_id": 1,
  "group_type": "investors",
  "emails": [
    "investor1@example.com",
    "investor2@example.com"
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "group_type": "investors",
  "emails": [
    "investor1@example.com",
    "investor2@example.com"
  ]
}
```

#### GET /audience/list

List all audience groups for a user.

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "group_type": "investors",
    "emails": ["investor1@example.com", "investor2@example.com"]
  },
  {
    "id": 2,
    "user_id": 1,
    "group_type": "employees",
    "emails": ["employee1@example.com", "employee2@example.com"]
  }
]
```

#### GET /audience/{group_id}

Get a specific audience group.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "group_type": "investors",
  "emails": ["investor1@example.com", "investor2@example.com"]
}
```

---

### Dashboard

#### GET /dashboard/{user_id}

Get user's public dashboard (HTML page).

**Response:** HTML page showing all sent updates

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Rate Limiting

Currently not implemented in MVP. For production, implement rate limiting using:
- FastAPI middleware
- Nginx rate limiting
- CloudFlare or similar CDN

## Best Practices

1. **Always validate user_id** before operations
2. **Handle errors gracefully** on the client side
3. **Use appropriate timeouts** for draft generation (may take 10-30 seconds)
4. **Batch operations** when possible
5. **Cache style profiles** after upload

## Example Workflows

### Complete Weekly Update Flow

```bash
# 1. Submit update
curl -X POST http://localhost:8000/update/submit \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "content": "Weekly update content..."}'

# 2. Generate drafts
curl -X POST http://localhost:8000/drafts/generate/1?user_id=1

# 3. Review and approve
curl -X POST http://localhost:8000/review/approve/1?user_id=1

# 4. Send to audience
curl -X POST http://localhost:8000/send/1?user_id=1
```

### Edit and Regenerate Flow

```bash
# 1. Apply natural language edits
curl -X POST http://localhost:8000/review/apply-edits/1 \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "edit_instructions": "Make it shorter"}'

# 2. Or regenerate completely
curl -X POST http://localhost:8000/review/regenerate/1?user_id=1
```

## Client Libraries

For easier integration, consider using:
- Python: `requests` or `httpx`
- JavaScript: `fetch` or `axios`
- TypeScript: Generated from OpenAPI spec

## Future Enhancements

Planned API improvements:
- JWT authentication
- WebSocket support for real-time draft generation
- Batch operations
- Webhook notifications
- API versioning
- GraphQL endpoint
