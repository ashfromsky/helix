# Helix

**AI-powered API mocking server with guaranteed schema compliance.**

Stop writing mock data manually. Define your schema once - Helix generates realistic data that **always matches your structure**.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-blue.svg)](https://fastapi.tiangolo.com/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

![Helix Demo](assets/images/Helix.png)

---

## Quick Start

### Option 1: CLI Setup (Recommended)

```bash
# Install Helix
git clone https://github.com/ashfromsky/helix.git
cd helix
pip install -e .

# Interactive setup wizard
helix init

# Start server
helix start
```

Visit `http://localhost:8000`

### Option 2: Docker (Fastest)

```bash
# Clone and start
git clone https://github.com/ashfromsky/helix.git
cd helix
docker-compose up
```

Visit `http://localhost:8080`

### Option 3: Manual Setup

```bash
# Clone repository
git clone https://github.com/ashfromsky/helix.git
cd helix

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy configuration
cp .env.example .env

# Start server
uvicorn app.main:app --reload --port 8080
```

### Want to Run Offline with Local LLM?

→ **[Jump to Ollama Setup](#ollama-local-ai)** for completely offline AI with no API keys.

---

## CLI Commands

Helix provides a powerful CLI for easy management:

### `helix init`

Interactive setup wizard that configures your environment:

```bash
helix init
```

**What it does:**
- Guides you through AI provider selection (demo/ollama/deepseek/groq)
- Configures API keys if needed
- Creates `.env` file automatically
- Sets up Redis container (if Docker available)
- Initializes AI system prompt
- Creates required directories

**Example output:**
```
AI-Powered API Mocking Platform
SETUP WIZARD

1. AI Provider Configuration
? Select AI provider: 
  → demo - Free, no API keys required
    ollama - Local LLM, private and unlimited
    deepseek - OpenRouter, cost-effective
    groq - Ultra-fast inference, free tier available

2. Environment Setup
✓ Configuration applied successfully
✓ Directory structure created
✓ AI system prompt initialized

3. Infrastructure
✓ Redis started successfully

Configuration Applied Successfully

Provider: DEMO
```

### `helix start`

Starts the Helix API server:

```bash
helix start [OPTIONS]
```

**Options:**
- `--host TEXT`: Host to bind to (default: 0.0.0.0)
- `--port INTEGER`: Port to bind to (default: 8000)
- `--reload / --no-reload`: Enable auto-reload (default: True)

**Examples:**
```bash
# Start with defaults
helix start

# Custom port
helix start --port 3000

# Production mode (no reload)
helix start --no-reload --port 8080
```

### `helix status`

Shows current configuration and system status:

```bash
helix status
```

**Example output:**
```
Configuration Status
CURRENT SETTINGS

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Parameter                    ┃ Value                                ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ AI Provider                  │ demo                                 │
│ Redis URL                    │ redis://localhost:6379               │
│ Server Port                  │ 8000                                 │
└──────────────────────────────┴──────────────────────────────────────┘
```

### `helix config`

Manage configuration interactively:

```bash
helix config
```

**Options:**
- **Change AI Provider**: Switch between demo/ollama/deepseek/groq
- **Update API Keys**: Update existing API credentials
- **Reset Configuration**: Delete and reconfigure from scratch
- **Exit**: Leave configuration unchanged

**Example session:**
```bash
helix config

Configuration Manager
MODIFY SETTINGS

? What would you like to configure?
  → Change AI Provider
    Update API Keys
    Reset Configuration
    Exit

? Select AI provider:
  → deepseek - OpenRouter, cost-effective

? OpenRouter API key: ****************************

✓ Provider configuration updated
```

### `helix --help`

Shows all available commands and options:

```bash
helix --help
```

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
- **CLI Interface** - Easy setup and management with `helix` commands

---

## Configuration

### Environment Variables

After running `helix init`, your `.env` file is automatically configured. You can also edit it manually:

```env
# AI Provider (demo/deepseek/groq/ollama)
HELIX_AI_PROVIDER=demo

# DeepSeek (via OpenRouter)
HELIX_OPENROUTER_API_KEY=sk-or-v1-your-key-here
HELIX_OPENROUTER_MODEL=deepseek/deepseek-chat

# Groq
HELIX_GROQ_API_KEY=gsk_your-key-here
HELIX_GROQ_MODEL=llama-3.1-70b-versatile

# Ollama (Local)
HELIX_OLLAMA_HOST=http://localhost:11434
HELIX_OLLAMA_MODEL=llama3

# Server Settings
HELIX_PORT=8080
HELIX_HOST=0.0.0.0
HELIX_DEBUG=true

# Redis
HELIX_REDIS_HOST=localhost
HELIX_REDIS_PORT=6379
```

### AI Providers

Choose your AI provider during `helix init` or change it later with `helix config`:

| Provider | Setup | Free Tier | Speed | Best For |
|----------|-------|-----------|-------|----------|
| **demo** (default) | None needed | ✓ Unlimited | Fast | Getting started |
| **DeepSeek** | API key required | 500 req/day | Medium | Production |
| **Groq** | API key required | 14,400 req/day | Ultra-fast | High volume |
| **Ollama** | Local installation | ✓ Unlimited | Varies | Offline/Privacy |

#### Demo Mode (Default)

No setup needed. Uses template-based generation with Faker library.

```bash
helix init
# Select: demo - Free, no API keys required
```

#### DeepSeek via OpenRouter

1. Run `helix init` or `helix config`
2. Select `deepseek`
3. Enter your OpenRouter API key from [openrouter.ai](https://openrouter.ai/)

```bash
helix config
# Select: Change AI Provider → deepseek
# Enter API key when prompted
```

#### Groq

1. Run `helix init` or `helix config`
2. Select `groq`
3. Enter your Groq API key from [console.groq.com](https://console.groq.com/)

```bash
helix config
# Select: Change AI Provider → groq
# Enter API key when prompted
```

#### Ollama (Local AI)

Ollama runs AI models locally - **no API keys, no rate limits, completely offline**.

**Quick Setup:**

```bash
# 1. Install Ollama
# Visit https://ollama.com/ and download for your OS

# 2. Pull a model
ollama pull llama3.2

# 3. Configure Helix
helix init
# Select: ollama - Local LLM, private and unlimited
# Enter Ollama host (default: http://localhost:11434)

# 4. Start Helix
helix start
```

**Model Recommendations:**

| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| `llama3.2:1b` | 1GB | 2GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Testing, demos |
| `llama3.2` | 2GB | 4GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | **Most users** |
| `llama3.1:8b` | 4.7GB | 8GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Production |
| `llama3.1:70b` | 40GB | 32GB+ | ⚡ | ⭐⭐⭐⭐⭐ | Maximum quality |

**Docker Setup:**

If using Docker, update your Ollama host:

```bash
helix config
# Select: Change AI Provider → ollama
# Host: http://host.docker.internal:11434
```

**Troubleshooting:**

```bash
# Check if Ollama is running
ollama list

# Start Ollama server
ollama serve

# Test connection
curl http://localhost:11434/api/tags

# Pull missing model
ollama pull llama3.2
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
}
```

**2. Define Schema in System Prompt:**

Edit `assets/AI/MOCKPILOT_SYSTEM.md` (created by `helix init`):

```markdown
## User Resource Schema
When handling /api/users endpoints:
- id: string (format: usr_XXXXXXXX)
- name: string (full name)
- email: string (valid email)
- role: enum [admin, user, guest]
- createdAt: ISO 8601 timestamp
```

**3. Helix Response (Always Matches Schema):**
```json
{
  "id": "usr_9Xk2LmNp",
  "name": "Sarah Chen",
  "email": "sarah.chen@company.com",
  "role": "admin",
  "createdAt": "2024-12-19T14:23:00Z"
}
```

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

## System Status

Check your current configuration anytime:

```bash
helix status
```

This shows:
- Active AI provider
- Redis connection status
- Server port
- API keys (masked)
- Model being used

---

## Troubleshooting

### Redis Connection Failed

```bash
# Check if setup completed
helix status

# Re-run setup if needed
helix init

# Or start Redis manually
docker run -d -p 6379:6379 redis:7-alpine
```

### AI Provider Errors

```bash
# Check current configuration
helix status

# Reconfigure provider
helix config
# Select: Change AI Provider

# Or fallback to demo mode
helix config
# Select: demo
```

### Configuration Issues

```bash
# Reset everything
helix config
# Select: Reset Configuration

# Then reconfigure
helix init
```

### CLI Not Found

```bash
# Reinstall Helix
pip install -e .

# Verify installation
helix --help
```

### Port Already in Use

```bash
# Use different port
helix start --port 3000

# Or kill existing process
lsof -ti:8080 | xargs kill -9
```

---

## Architecture

```
helix/
├── app/
│   ├── cli.py                           # CLI commands (helix init/start/status)
│   ├── cliAssets/                       # CLI resources (logo, prompts)
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
├── pyproject.toml                       # CLI setup configuration
├── docker-compose.yml                   # Container orchestration
└── .env                                 # Configuration (created by helix init)
```

---

## Requirements

- **Python**: 3.11+
- **Redis**: 7.0+ (via Docker or local)
- **Docker**: Optional but recommended
- **Ollama**: Optional (for local AI)

---

## Development

### Install for Development

```bash
# Clone repository
git clone https://github.com/ashfromsky/helix.git
cd helix

# Install in editable mode with dev dependencies
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Format code
black app/
isort app/

# Type checking
mypy app/
```

### CLI Development

The CLI is built with Typer and Rich. Main commands are in `app/cli.py`:

- `helix init`: Setup wizard (`init()` function)
- `helix start`: Server launcher (`start()` function)
- `helix status`: Configuration viewer (`status()` function)
- `helix config`: Configuration manager (`config()` function)

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

Built with ❤️ for developers who want to focus on features, not infrastructure.