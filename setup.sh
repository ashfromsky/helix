#!/bin/bash

echo "🌀 Helix Setup Script"
echo "====================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo ""
    echo "✓ .env file already exists"
fi

echo ""
echo "Creating directories..."
mkdir -p assets/AI
mkdir -p templates/default_pages
mkdir -p tests

if [ ! -f assets/AI/MOCKPILOT_SYSTEM.md ]; then
    cat > assets/AI/MOCKPILOT_SYSTEM.md << 'EOF'
# Role
You are **MockPilot AI**, an intelligent API mocking engine. Your goal is to act as a production-ready backend server. When you receive an HTTP method, a URL path, and an optional body, you must generate a realistic, valid JSON response that a real API would return.

# Objectives
1. **Analyze the Request:** Look at the Method (GET, POST, etc.) and the Path (e.g., `/api/v1/users`). Infer the resource structure.
2. **Generate Realistic Data:** Do not use placeholder text like "foo", "bar", or "test". Use realistic names (e.g., "John Doe"), addresses, ISO 8601 dates, and professional IDs (e.g., "usr_8Jk2...").
3. **Respect REST Standards:**
   * `GET` collection -> Return an array of objects.
   * `GET` single item -> Return a single object.
   * `POST` -> Return the created object with status `201`.
   * `DELETE` -> Return empty body or success message with status `200` or `204`.
   * `PUT/PATCH` -> Return the updated object.
4. **Handle Context:** If the user sends a body (e.g., `{"name": "Alice"}`), the response MUST reflect this data (e.g., the created user should be named "Alice").

# Output Format (STRICT)
You must output **ONLY** a valid JSON object. No conversational text.

The JSON structure must be exactly:
```json
{
  "status_code": <integer>,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": <json_data>
}
```
EOF
    echo "✓ Created MOCKPILOT_SYSTEM.md"
fi

echo ""
if command -v docker &> /dev/null; then
    echo "✓ Docker found: $(docker --version)"

    if docker ps | grep -q helix-redis; then
        echo "✓ Redis container is already running"
    else
        echo "Starting Redis container..."
        docker run -d -p 6379:6379 --name helix-redis redis:7-alpine
        echo "✓ Redis started"
    fi
else
    echo "⚠️  Docker not found. You'll need Redis installed separately."
fi

echo ""
echo "========================"
echo "✅ Setup Complete!"
echo "========================"
echo ""
echo "To start Helix:"
echo "  1. Activate venv:  source venv/bin/activate"
echo "  2. Run server:     uvicorn app.main:app --reload --port 8080"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up"
echo ""
echo "Then visit: http://localhost:8080"
echo ""