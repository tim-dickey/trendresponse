# TrendResponse Setup Guide

This guide walks you through setting up the TrendResponse project from scratch.

## Prerequisites

1. **Python 3.11 or higher**
   ```bash
   python --version  # Should be 3.11+
   ```

2. **GitHub Personal Access Token**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `read:org`
   - Copy the token (starts with `ghp_`)

3. **LinkedIn Developer Account** (for LinkedIn integration)
   - Go to https://www.linkedin.com/developers/
   - Create a new app
   - Note your Client ID and Client Secret
   - Add redirect URI: `http://localhost:8000/auth/linkedin/callback`

## Quick Start

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/tim-dickey/trendresponse.git
cd trendresponse

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Required:
# - GITHUB_TOKEN: Your GitHub PAT
# - LINKEDIN_CLIENT_ID: From LinkedIn Developer Portal
# - LINKEDIN_CLIENT_SECRET: From LinkedIn Developer Portal
# - SECRET_KEY: Generate with: python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Run the Application

```bash
# Start the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Access API docs at: http://localhost:8000/docs
```

## Docker Setup (Recommended)

### 1. Using Docker Compose

```bash
# Create .env file (same as above)
cp .env.example .env
# Edit .env with your credentials

# Start all services (API, PostgreSQL, Redis)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### 2. Docker Only

```bash
# Build image
docker build -t trendresponse:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e GITHUB_TOKEN=your_token \
  -e LINKEDIN_CLIENT_ID=your_client_id \
  -e LINKEDIN_CLIENT_SECRET=your_secret \
  -e SECRET_KEY=your_secret_key \
  trendresponse:latest
```

## Testing AI Suggestions

Once the server is running, you can test the AI suggestion feature:

```bash
# Note: /comments/validate requires authentication (Authorization: Bearer <token>).
# A full token issuance flow is not yet available for the MVP, so this endpoint
# cannot be exercised without a valid JWT. Once authentication is implemented,
# use the following:

# Test comment validation (requires a valid auth token)
curl -X POST "http://localhost:8000/comments/validate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token_here>" \
  -d '{"content": "This is a test comment with exactly ten words here"}'

# Expected response:
# {"valid": true, "word_count": 10, "message": "Comment is valid"}
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_suggestions.py -v

# Run and show print statements
pytest -s tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
ruff check src/ tests/

# Run all quality checks
black src/ tests/ && isort src/ tests/ && ruff check src/ tests/
```

## GitHub Models Setup

The application uses **GitHub Models** (free tier) for AI-powered suggestions:

1. **GitHub Token Requirements:**
   - Your GitHub PAT needs `repo` scope
   - Free tier includes: 15 requests/minute, 150 requests/hour
   - Upgrade to paid for higher limits

2. **Available Models:**
   - Default: `openai/gpt-4.1-mini` (fast, cost-effective)
   - Alternatives: `openai/gpt-4.1`, `openai/o1-mini`
   - Change via `MODEL_NAME` in `.env`

3. **Test the Model:**
   ```bash
   # Test API access
   curl https://models.github.ai/inference/chat/completions \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "openai/gpt-4.1-mini",
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
   ```

## Troubleshooting

### Issue: "Could not validate credentials"
- **Solution**: Generate a new SECRET_KEY or check your .env file is loaded

### Issue: "GitHub API rate limit exceeded"
- **Solution**: Wait for rate limit reset or upgrade GitHub subscription

### Issue: Database errors
- **If using local SQLite** (default `DATABASE_URL`): Delete `trendresponse.db` and restart (dev only)
- **If using Docker Compose with PostgreSQL**: Run `docker-compose down -v` to remove volumes and reinitialise the database, then `docker-compose up -d`

### Issue: Docker container won't start
- **Solution**: Check logs with `docker-compose logs api`
- Verify all environment variables are set

## Next Steps

1. **Explore API Documentation**
   - Open http://localhost:8000/docs in your browser
   - Try the interactive Swagger UI

2. **Set Up LinkedIn OAuth**
   - Complete LinkedIn app configuration
   - Test the OAuth flow at `/auth/linkedin/callback`

3. **Add Sample Data**
   - Seed the database with sample posts for testing
   - Create a seed script and add it to `scripts/` as needed

4. **Deploy to Production**
   - Options: AWS Lambda, Heroku, Azure Container Apps

## Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **GitHub Models**: https://github.com/marketplace/models
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LinkedIn API**: https://learn.microsoft.com/en-us/linkedin/

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the comprehensive README.md
