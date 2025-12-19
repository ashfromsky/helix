# SCHEMAS.md - API Schema Cookbook

> **Ready-to-use schema templates for Helix**  
> Copy these examples into your system prompts or request bodies to enforce strict data structures.

---

## How to Use These Schemas

### Method 1: System Prompt (Recommended for AI Providers)
Add this to your custom system prompt in `assets/AI/MOCKPILOT_SYSTEM.md`:

```markdown
CRITICAL: You MUST return responses matching this exact schema:
[paste schema from below]
```

### Method 2: Request Body Hints
When making POST/PUT requests, include schema hints in your body:

```json
{
  "_schema": "User",
  "id": "",
  "email": "",
  "name": ""
}
```

Helix will generate values that match the field names and types.

---

## Authentication & Users

### User Schema (Standard)

```json
{
  "id": "usr_a1b2c3d4",
  "email": "user@example.com",
  "username": "johndoe",
  "name": "John Doe",
  "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=abc",
  "role": "user",
  "status": "active",
  "created_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}
```

**Field Guarantees:**
- `id`: Always starts with `usr_` prefix
- `email`: Valid email format (RFC 5322)
- `role`: Enum: `["admin", "user", "moderator", "guest"]`
- `status`: Enum: `["active", "inactive", "pending", "suspended"]`
- `created_at` / `updated_at`: ISO 8601 format with timezone

---

### Authentication Response (JWT)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "usr_a1b2c3d4",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }
}
```

**Field Guarantees:**
- `access_token`: Valid JWT format (3 base64 segments separated by dots)
- `expires_in`: Integer (seconds)
- `token_type`: Always `"Bearer"`

---

### User Registration Request

```json
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "password_confirmation": "SecurePass123!",
  "name": "Jane Smith",
  "terms_accepted": true
}
```

**Response (201 Created):**
```json
{
  "id": "usr_xyz789",
  "email": "newuser@example.com",
  "name": "Jane Smith",
  "status": "pending",
  "verification_email_sent": true,
  "created_at": "2024-12-19T10:30:00Z"
}
```

---

## 🛒 E-Commerce

### Product Schema

```json
{
  "id": "prod_a1b2c3d4",
  "sku": "ABC-12345",
  "name": "Wireless Headphones",
  "description": "Premium noise-cancelling wireless headphones",
  "price": 149.99,
  "currency": "USD",
  "category": "Electronics",
  "subcategory": "Audio",
  "brand": "TechBrand",
  "in_stock": true,
  "stock_quantity": 47,
  "images": [
    "https://cdn.example.com/products/headphones-1.jpg",
    "https://cdn.example.com/products/headphones-2.jpg"
  ],
  "specifications": {
    "color": "Black",
    "weight": "250g",
    "battery_life": "30 hours",
    "bluetooth_version": "5.2"
  },
  "rating": 4.7,
  "reviews_count": 328,
  "created_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}
```

**Field Guarantees:**
- `id`: Starts with `prod_`
- `sku`: Alphanumeric with hyphens
- `price`: Decimal with 2 places
- `currency`: ISO 4217 code
- `rating`: Float between 0.0 and 5.0
- `in_stock`: Boolean

---

### Order Schema

```json
{
  "id": "ord_a1b2c3d4",
  "order_number": "ORD-20241219-001",
  "customer_id": "usr_xyz789",
  "status": "processing",
  "subtotal": 299.98,
  "tax": 24.00,
  "shipping": 9.99,
  "total": 333.97,
  "currency": "USD",
  "items": [
    {
      "id": "item_001",
      "product_id": "prod_a1b2c3d4",
      "product_name": "Wireless Headphones",
      "quantity": 2,
      "unit_price": 149.99,
      "total": 299.98
    }
  ],
  "shipping_address": {
    "full_name": "John Doe",
    "street_line1": "123 Main Street",
    "street_line2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "USA",
    "phone": "+1 (555) 123-4567"
  },
  "payment_method": "credit_card",
  "payment_status": "paid",
  "tracking_number": "1Z999AA10123456784",
  "created_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}
```

**Field Guarantees:**
- `status`: Enum: `["pending", "processing", "shipped", "delivered", "cancelled"]`
- `payment_status`: Enum: `["pending", "paid", "failed", "refunded"]`
- All monetary values: Decimals with 2 places
- `order_number`: Format `ORD-YYYYMMDD-NNN`

---

## Content Management

### Blog Post Schema

```json
{
  "id": "post_a1b2c3d4",
  "title": "Getting Started with Helix",
  "slug": "getting-started-with-helix",
  "excerpt": "Learn how to set up and use Helix in your projects",
  "content": "Full markdown content here...",
  "author": {
    "id": "usr_xyz789",
    "name": "Jane Smith",
    "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=jane"
  },
  "status": "published",
  "category": "Tutorials",
  "tags": ["helix", "api", "tutorial"],
  "featured_image": "https://cdn.example.com/blog/helix-intro.jpg",
  "views": 1247,
  "likes": 89,
  "comments_count": 23,
  "published_at": "2024-12-19T10:30:00Z",
  "created_at": "2024-12-18T14:20:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}
```

**Field Guarantees:**
- `slug`: URL-safe lowercase with hyphens
- `status`: Enum: `["draft", "published", "archived"]`
- `tags`: Array of strings

---

### Comment Schema

```json
{
  "id": "cmt_a1b2c3d4",
  "post_id": "post_xyz789",
  "author": {
    "id": "usr_abc123",
    "name": "Michael Brown",
    "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=michael"
  },
  "content": "Great article! This helped me a lot.",
  "parent_id": null,
  "status": "approved",
  "likes": 5,
  "created_at": "2024-12-19T11:00:00Z",
  "updated_at": "2024-12-19T11:00:00Z"
}
```

---

## Task Management

### Task Schema

```json
{
  "id": "task_a1b2c3d4",
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API",
  "status": "in_progress",
  "priority": "high",
  "assignee": {
    "id": "usr_xyz789",
    "name": "Sarah Johnson",
    "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=sarah"
  },
  "project_id": "proj_abc123",
  "labels": ["backend", "security", "urgent"],
  "due_date": "2024-12-25T23:59:59Z",
  "estimated_hours": 8,
  "actual_hours": 3.5,
  "progress": 45,
  "created_by": "usr_admin",
  "created_at": "2024-12-15T09:00:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}
```

**Field Guarantees:**
- `status`: Enum: `["todo", "in_progress", "review", "done", "blocked"]`
- `priority`: Enum: `["low", "medium", "high", "urgent"]`
- `progress`: Integer 0-100

---

## Error Responses

### Standard Error Schema

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested user could not be found",
    "details": {
      "resource": "User",
      "id": "usr_nonexistent"
    },
    "timestamp": "2024-12-19T10:30:00Z",
    "request_id": "req_a1b2c3d4"
  }
}
```

**Common Error Codes:**
- `VALIDATION_ERROR` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `RESOURCE_NOT_FOUND` (404)
- `CONFLICT` (409)
- `INTERNAL_SERVER_ERROR` (500)

---

### Validation Error Schema (422)

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "fields": [
      {
        "field": "email",
        "message": "Email is required",
        "code": "REQUIRED_FIELD"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters",
        "code": "MIN_LENGTH",
        "params": { "min": 8 }
      }
    ],
    "timestamp": "2024-12-19T10:30:00Z",
    "request_id": "req_xyz789"
  }
}
```

---

## Pagination

### Paginated Response Schema

```json
{
  "data": [
    { "id": "usr_001", "name": "User 1" },
    { "id": "usr_002", "name": "User 2" }
  ],
  "pagination": {
    "total": 247,
    "page": 1,
    "per_page": 20,
    "total_pages": 13,
    "has_next": true,
    "has_prev": false
  },
  "links": {
    "first": "/api/users?page=1",
    "last": "/api/users?page=13",
    "next": "/api/users?page=2",
    "prev": null
  }
}
```

---

## Security Notes

### Sensitive Data Handling

**Never include these in responses (Helix will generate mock versions):**
- Real passwords (use `hashed_password` or omit entirely)
- Real credit card numbers (use `****1234` format)
- Real SSNs or government IDs
- Real API keys or tokens in examples

**Example Safe Response:**
```json
{
  "id": "usr_a1b2c3d4",
  "email": "user@example.com",
  "hashed_password": "$2b$12$abcdef...",
  "payment_method": {
    "type": "credit_card",
    "last_four": "1234",
    "brand": "Visa",
    "exp_month": 12,
    "exp_year": 2025
  }
}
```

---

## Custom Schema Instructions for AI

To enforce a custom schema with AI providers (DeepSeek, Groq), modify your system prompt:

```markdown
You are MockPilot AI. When generating responses, follow these rules:

1. ALWAYS match the exact structure provided below
2. Use realistic data that matches field semantics
3. Respect data types strictly (string, number, boolean, object, array)
4. Follow enum constraints exactly

SCHEMA DEFINITION:
{
  "id": "string (format: prefix_alphanumeric)",
  "name": "string",
  "email": "string (format: valid_email)",
  "status": "string (enum: active|inactive|pending)",
  "created_at": "string (format: ISO8601)",
  "metadata": "object (free-form JSON)"
}

EXAMPLE OUTPUT:
{
  "status_code": 200,
  "headers": {"Content-Type": "application/json"},
  "body": {
    "id": "usr_a1b2c3d4",
    "name": "John Doe",
    "email": "john@example.com",
    "status": "active",
    "created_at": "2024-12-19T10:30:00Z",
    "metadata": {}
  }
}
```

---

## Additional Resources

- **Faker Library**: Helix's demo mode uses Faker for realistic data
- **REST Standards**: All schemas follow REST/HTTP best practices
- **JSON Schema**: Consider validating responses with JSON Schema for production use

---

**Need a schema that's not here?** Open an issue on GitHub with your use case!