# Helix

**AI-powered API mocking server with guaranteed schema compliance.**

Stop writing mock data manually. Define your schema once - Helix generates realistic data that **always matches your structure**.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-blue.svg)](https://fastapi.tiangolo.com/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

![Helix Demo](assets/images/Helix.png)

---

## Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/ashfromsky/helix.git
cd helix

# Start services
docker-compose up
```

Visit `http://localhost:8080`

### Local Setup

```bash
# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Start server
uvicorn app.main:app --reload --port 8080
```

### Want to Run Offline with Local LLM?

→ **[Jump to Ollama Setup](#ollama-local-ai)** for completely offline AI with no API keys.

---

## How It Works

Helix uses your `MOCKPILOT_SYSTEM.md` rules to strictly follow your API design.

**Basic Mode (No Schema):**
```bash
# Helix infers structure from path and method
curl http://localhost:8080/api/users
# Returns: realistic user data
```

**Schema Mode (Guaranteed Structure):**
```bash
# 1. Define your schema
POST /api/users
Body: {
  "schema": {
    "id": "string",
    "name": "string",
    "email": "string",
    "role": "admin|user|guest"
  }
}

# 2. Helix generates data matching your schema exactly
# Every field, every type, every enum value - guaranteed
```

**The key difference:** 
- **Without schema**: Helix makes smart guesses (great for demos)
- **With schema**: Helix enforces exact structure (safe for production)

---

## Features

- **Schema Enforcement** - Define structure once, get consistent data forever ([see below](#schema-enforcement))
- **Zero Configuration** - Hit any endpoint and get instant responses
- **AI-Powered** - Uses DeepSeek, Groq, Ollama, or built-in templates
- **Context Aware** - Remembers your actions within sessions
- **Smart Data** - Generates realistic names, emails, dates, IDs
- **REST Compatible** - Follows HTTP standards automatically
- **Redis Caching** - Fast responses with intelligent caching
- **Chaos Engineering** - Simulate failures and latency
- **Live Dashboard** - Monitor requests in real-time

---

## Schema Enforcement

**Problem:** Random JSON structures break your frontend.

**Solution:** Define your schema - Helix guarantees compliance.

### Example: TypeScript Interface → Guaranteed JSON

**1. Your TypeScript Interface:**
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: string; // ISO 8601
  metadata: {
    lastLogin: string;
    loginCount: number;
  }
}
```

**2. Send Schema to Helix:**
```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "id": "string",
      "name": "string", 
      "email": "string",
      "role": "admin|user|guest",
      "createdAt": "iso8601",
      "metadata": {
        "lastLogin": "iso8601",
        "loginCount": "number"
      }
    }
  }'
```

**3. Helix Response (Always Matches Schema):**
```json
{
  "id": "usr_9Xk2LmNp",
  "name": "Sarah Chen",
  "email": "sarah.chen@company.com",
  "role": "admin",
  "createdAt": "2024-12-19T14:23:00Z",
  "metadata": {
    "lastLogin": "2024-12-19T09:15:00Z",
    "loginCount": 47
  }
}
```

**4. Every Subsequent Request Uses This Schema:**
```bash
curl http://localhost:8080/api/users/123
# Same structure guaranteed
```

### Schema Formats Supported

**1. JSON Schema (Recommended):**
```json
{
  "schema": {
    "type": "object",
    "properties": {
      "id": { "type": "string", "pattern": "^usr_[a-zA-Z0-9]{8}$" },
      "name": { "type": "string" },
      "age": { "type": "integer", "minimum": 18, "maximum": 100 }
    },
    "required": ["id", "name"]
  }
}
```

**2. Simple Type Definitions:**
```json
{
  "schema": {
    "id": "string",
    "name": "string",
    "age": "number",
    "active": "boolean",
    "role": "admin|user|guest"
  }
}
```

**3. OpenAPI Schema:**
```yaml
# Place in assets/AI/SCHEMAS/users.yaml
openapi: 3.0.0
components:
  schemas:
    User:
      type: object
      properties:
        id: 
          type: string
        name:
          type: string
```

### Inline Schema Definition

Edit `assets/AI/MOCKPILOT_SYSTEM.md` to define schemas:

```markdown
## User Resource Schema
When handling /api/users endpoints:
- id: string (format: usr_XXXXXXXX)
- name: string (full name)
- email: string (valid email)
- role: enum [admin, user, guest]
- createdAt: ISO 8601 timestamp
```

### Schema Validation

```bash
# Enable strict validation
HELIX_SCHEMA_VALIDATION=strict  # Reject invalid responses
HELIX_SCHEMA_VALIDATION=warn    # Log warnings only (default)
HELIX_SCHEMA_VALIDATION=off     # Disable validation
```

### Why This Matters

❌ **Without Schema:**
```json
// Request 1
{"id": 123, "userName": "Alice"}

// Request 2  
{"userId": "abc", "name": "Bob"}

// Your frontend breaks
```

✅ **With Schema:**
```json
// Request 1
{"id": "usr_123", "name": "Alice"}

// Request 2
{"id": "usr_456", "name": "Bob"}

// Consistent structure = happy frontend
```

---

## Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### AI Providers

Helix supports multiple AI providers. Choose one in `.env`:

| Provider | Setup | Free Tier | Speed | Best For |
|----------|-------|-----------|-------|----------|
| **demo** (default) | None needed | ✓ Unlimited | Fast | Getting started |
| **DeepSeek** | API key required | 500 req/day | Medium | Production |
| **Groq** | API key required | 14,400 req/day | Ultra-fast | High volume |
| **Ollama** | Local installation | ✓ Unlimited | Varies | Offline/Privacy |

#### Demo Mode (Default)

No setup needed. Uses template-based generation:

```env
HELIX_AI_PROVIDER=demo
```

#### DeepSeek via OpenRouter

1. Sign up at [https://openrouter.ai/](https://openrouter.ai/)
2. Get your API key
3. Configure `.env`:

```env
HELIX_AI_PROVIDER=deepseek
HELIX_OPENROUTER_API_KEY=sk-or-v1-your-key-here
HELIX_OPENROUTER_MODEL=deepseek/deepseek-chat
```

#### Groq

1. Sign up at [https://console.groq.com/](https://console.groq.com/)
2. Get your API key
3. Configure `.env`:

```env
HELIX_AI_PROVIDER=groq
HELIX_GROQ_API_KEY=gsk_your-key-here
HELIX_GROQ_MODEL=llama-3.1-70b-versatile
```

#### Ollama (Local AI)

Ollama runs AI models locally on your machine - **no API keys, no rate limits, completely offline**.

**Why Ollama?**
- ✓ 100% offline - no internet required
- ✓ No API keys or rate limits
- ✓ Complete data privacy
- ✓ Free forever
- ✓ Runs on your hardware

**Step 1: Install Ollama**

Visit [https://ollama.com/](https://ollama.com/) and download for your OS:

**macOS:**
```bash
# Download from https://ollama.com/download/mac
# Or use Homebrew
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
```bash
# Download installer from https://ollama.com/download/windows
```

**Step 2: Download a Model**

```bash
# Recommended: Llama 3.2 (2GB) - Best for most users
ollama pull llama3.2

# Alternatives:
ollama pull llama3.2:1b    # Tiny, very fast (1GB)
ollama pull llama3.2:3b    # Small, fast (2GB) 
ollama pull llama3.1:8b    # Balanced (4.7GB)
ollama pull llama3.1:70b   # Powerful, slow (40GB, needs 32GB+ RAM)
ollama pull mistral        # Alternative (4.1GB)
ollama pull codellama      # Code-specialized (3.8GB)
```

**Model Comparison:**

| Model | Size | RAM Needed | Speed | Quality | Best For |
|-------|------|------------|-------|---------|----------|
| `llama3.2:1b` | 1GB | 2GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Testing, demos |
| `llama3.2` | 2GB | 4GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | **Most users** |
| `llama3.1:8b` | 4.7GB | 8GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Production |
| `llama3.1:70b` | 40GB | 32GB+ | ⚡ | ⭐⭐⭐⭐⭐ | Maximum quality |
| `mistral` | 4.1GB | 8GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Alternative |
| `codellama` | 3.8GB | 8GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | API schemas |

**Step 3: Start Ollama Server**

```bash
# Usually starts automatically, but you can verify:
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

**Step 4: Configure Helix**

Edit `.env`:

```env
HELIX_AI_PROVIDER=ollama
HELIX_OLLAMA_MODEL=llama3.2

# --- OPTION 1: Local Setup (Default) ---
# Use this if running python main.py
HELIX_OLLAMA_HOST=http://localhost:11434

# --- OPTION 2: Docker Setup ---
# Use this if running via Docker Desktop
# HELIX_OLLAMA_HOST=http://host.docker.internal:11434

```
**Step 5: Test It Works**

```bash
# Test Ollama directly
ollama run llama3.2 "Generate a JSON user object"

# Test through Helix
curl http://localhost:8080/api/users

# Check Helix is using Ollama
curl http://localhost:8080/status
```

**Troubleshooting Ollama:**

```bash
# Problem: "connection refused"
# Solution: Check if Ollama is running
ps aux | grep ollama
ollama serve

# Problem: "model not found"  
# Solution: List and download models
ollama list
ollama pull llama3.2

# Problem: Slow responses
# Solution: Use smaller model
ollama pull llama3.2:1b

# Problem: Out of memory
# Solution: Close other apps or use smaller model
# Llama3.2:1b only needs 2GB RAM

# View logs (macOS/Linux)
cat ~/.ollama/logs/server.log

# View logs (Windows)
# Check %LOCALAPPDATA%\Ollama\logs\
```

**Performance Tips:**

```bash
# 1. Use smaller models for faster responses
HELIX_OLLAMA_MODEL=llama3.2:1b

# 2. Reduce token limit
HELIX_AI_MAX_TOKENS=500

# 3. Lower temperature for more consistent output
HELIX_AI_TEMPERATURE=0.3

# 4. Enable aggressive caching
HELIX_CACHE_TTL=7200  # 2 hours
```

**Complete Offline Setup:**

```bash
# 1. Download model once (with internet)
ollama pull llama3.2

# 2. Disconnect from internet

# 3. Start Helix
docker-compose up

# 4. Everything works offline
curl http://localhost:8080/api/users
```

---

## Usage Examples

### Basic CRUD Operations

```bash
# GET collection
curl http://localhost:8080/api/products

# GET single item
curl http://localhost:8080/api/products/prod_123

# POST (create)
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999}'

# PUT (full update)
curl -X PUT http://localhost:8080/api/products/prod_123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop", "price": 1499}'

# PATCH (partial update)
curl -X PATCH http://localhost:8080/api/products/prod_123 \
  -H "Content-Type: application/json" \
  -d '{"price": 1299}'

# DELETE
curl -X DELETE http://localhost:8080/api/products/prod_123
```

### Using Sessions

Maintain context across requests with `X-Session-ID` header:

```bash
# Session 1: Create a user
curl -H "X-Session-ID: session-1" \
  -X POST http://localhost:8080/api/users \
  -d '{"name": "Alice"}'

# Session 1: List users - returns Alice
curl -H "X-Session-ID: session-1" \
  http://localhost:8080/api/users

# Session 2: List users - returns different data
curl -H "X-Session-ID: session-2" \
  http://localhost:8080/api/users
```

### Recognized Resource Types

Helix generates appropriate data based on resource names:

| Resource | Generated Fields |
|----------|------------------|
| `users`, `accounts` | name, email, username, avatar, role, status |
| `products`, `items` | name, price, sku, in_stock, category |
| `orders` | order_number, total, status, items_count |
| `posts`, `articles` | title, content, author, published, views |
| `tasks`, `todos` | title, status, priority, due_date |
| `events` | title, start_time, end_time, location |
| `companies` | name, industry, employees_count, address |

---

## Advanced Features

### Chaos Engineering

Simulate production failures to test error handling:

```env
HELIX_CHAOS_ENABLED=true
HELIX_CHAOS_ERROR_RATE=0.1        # 10% requests fail
HELIX_CHAOS_LATENCY_RATE=0.15     # 15% requests delayed
HELIX_CHAOS_MIN_DELAY_MS=2000     # Min delay: 2s
HELIX_CHAOS_MAX_DELAY_MS=5000     # Max delay: 5s
```

### OpenAPI Spec Generation

Generate OpenAPI specification from your traffic:

```bash
# Make some requests first
curl http://localhost:8080/api/users
curl http://localhost:8080/api/products

# Generate spec
curl http://localhost:8080/api/generate-spec?limit=50
```

### Live Dashboard

Monitor all requests in real-time:

```
http://localhost:8080/dashboard
```

Features:
- Live request logging
- Method, path, status, latency
- Request/response inspection
- Clear logs

### Health Monitoring

```bash
# Quick health check
curl http://localhost:8080/health

# Detailed status
curl http://localhost:8080/status
```

---

## API Reference

### System Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/health` | GET | Health check |
| `/status` | GET | Detailed system status |
| `/dashboard` | GET | Live request dashboard |
| `/docs` | GET | Swagger API documentation |
| `/api/generate-spec` | GET | Generate OpenAPI spec |

### Dynamic Endpoints

| Pattern | Methods | Description |
|---------|---------|-------------|
| `/{any_path}` | GET | List collection or get single item |
| `/{any_path}` | POST | Create new resource |
| `/{any_path}` | PUT | Full update of resource |
| `/{any_path}` | PATCH | Partial update of resource |
| `/{any_path}` | DELETE | Delete resource |

**Examples:**
- `GET /api/v1/users` → List users
- `GET /api/users/123` → Get user 123
- `POST /orders` → Create order
- `DELETE /products/abc` → Delete product

---

## Architecture

```
helix/
├── app/
│   ├── routes/
│   │   ├── requestbased/catch_all.py    # Dynamic mock handler
│   │   └── ui/                          # Web interface
│   ├── services/
│   │   ├── ai/
│   │   │   ├── providers/               # AI provider implementations
│   │   │   │   ├── demo.py             # Template-based (default)
│   │   │   │   ├── deepseek.py         # DeepSeek via OpenRouter
│   │   │   │   ├── groq.py             # Groq inference
│   │   │   │   └── ollama.py           # Local Ollama
│   │   │   └── manager.py              # Provider manager
│   │   ├── cache.py                     # Redis caching
│   │   ├── context.py                   # Session management
│   │   └── logger.py                    # Request logging
│   └── main.py                          # FastAPI application
├── assets/AI/MOCKPILOT_SYSTEM.md        # AI system prompt (schema rules)
├── templates/                           # HTML templates
├── docker-compose.yml                   # Container orchestration
└── .env                                 # Configuration
```

---

## Requirements

- **Python**: 3.11+
- **Redis**: 7.0+ (via Docker or local)
- **Docker**: Optional but recommended
- **Ollama**: Optional (for local AI)

---

## Troubleshooting

### Redis Connection Failed

```bash
# Check Redis is running
docker ps | grep redis

# Start Redis manually
docker run -d -p 6379:6379 redis:7-alpine
```

### AI Provider Errors

```bash
# Check current provider status
curl http://localhost:8080/status

# Fallback to demo mode
# Edit .env: HELIX_AI_PROVIDER=demo
```

### Ollama Not Working

```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Check if model is downloaded
ollama list

# Pull model if missing
ollama pull llama3.2

# Restart Ollama
killall ollama
ollama serve
```

### Port Already in Use

```bash
# Change port in .env
HELIX_PORT=8081

# Or kill existing process
lsof -ti:8080 | xargs kill -9
```

### Schema Not Being Enforced

```bash
# Check schema validation is enabled
grep SCHEMA_VALIDATION .env

# Verify schema is in MOCKPILOT_SYSTEM.md
cat assets/AI/MOCKPILOT_SYSTEM.md

# Clear cache to force schema reload
curl -X DELETE http://localhost:8080/api/cache/clear
```

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)**

This project is free and open-source software. See [LICENSE](LICENSE) for details.

Key points:
- ✓ Free to use, modify, and distribute
- ✓ Must disclose source code
- ✓ Network use = distribution (AGPL requirement)
- ✓ Same license for derivatives

---

## Links

- **GitHub**: [https://github.com/ashfromsky/helix](https://github.com/ashfromsky/helix)
- **Issues**: [https://github.com/ashfromsky/helix/issues](https://github.com/ashfromsky/helix/issues)
- **Discussions**: [https://github.com/ashfromsky/helix/discussions](https://github.com/ashfromsky/helix/discussions)

---

**Schema-safe mocking for serious development.**
