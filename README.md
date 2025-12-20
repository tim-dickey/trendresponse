# TrendResponse

<div align="center">

**AI-Powered Social Media Rapid-Response Platform**

*Engage on trending posts with concise, AI-suggested comments in seconds*

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🚀 Overview

TrendResponse helps professionals maintain social media presence without the time investment. Powered by GitHub AI models, it generates concise, thoughtful 10-25 word comments on trending posts, reducing composition time by 80%.

### Key Features

- **🤖 AI-Powered Suggestions**: Generate 3-5 contextual comment options using GPT-4.1-mini
- **⚡ Rapid Composition**: Create comments in <30 seconds vs 3-5 minutes manually
- **📏 Constraint Enforcement**: Automatic 10-25 word validation for concise engagement
- **🔄 Multi-Platform Ready**: Modular architecture supporting LinkedIn, Twitter, and more
- **💰 Cost-Effective**: Free tier with GitHub Models, scales affordably
- **🐳 Containerized**: Docker-ready for cloud-agnostic deployment

---

## 📋 Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose** (optional, for containerized deployment)
- **GitHub Personal Access Token** (for free AI model access)
- **LinkedIn OAuth Credentials** (for LinkedIn integration)

---

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tim-dickey/trendresponse.git
cd trendresponse
```

### 2. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials:
# - GITHUB_TOKEN: Your GitHub Personal Access Token (https://github.com/settings/tokens)
# - LINKEDIN_CLIENT_ID & SECRET: From LinkedIn Developer Portal
# - SECRET_KEY: Generate with: openssl rand -hex 32
```

### 3. Install Dependencies

**Option A: Local Development**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional, for NLP features)
python -m spacy download en_core_web_sm
```

**Option B: Docker (Recommended)**

```bash
docker-compose up -d
```

### 4. Run the Application

**Local:**

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Docker:**

```bash
docker-compose up
```

### 5. Access the API

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **Health Check**: http://localhost:8000/health

---

## 🎯 Usage

### Generate Comment Suggestions

```bash
curl -X POST "http://localhost:8000/comments/suggest" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": "linkedin-post-123",
    "num_suggestions": 3
  }'
```

**Response:**

```json
{
  "suggestions": [
    "Fascinating perspective on remote work dynamics. How do you balance async communication with team cohesion?",
    "This aligns with recent studies showing productivity gains. Have you measured impact on employee satisfaction?",
    "Great insights! We've seen similar patterns. What tools do you recommend for distributed collaboration?"
  ]
}
```

### Validate Comment

```bash
curl -X POST "http://localhost:8000/comments/validate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a test comment with exactly fifteen words in total for validation purposes."
  }'
```

### Post Comment

```bash
curl -X POST "http://localhost:8000/comments/post" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": "linkedin-post-123",
    "content": "Insightful analysis! How do you see this evolving with emerging AI capabilities?",
    "platform": "linkedin"
  }'
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│ Presentation Layer (FastAPI + Swagger UI)           │
│ - Dashboard: Trending posts feed                    │
│ - Composer: Constrained input (10-25 words)         │
│ - Suggestions: AI-powered recommendations           │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ Logic Layer (Python Backend)                        │
│ - Feed aggregation (LinkedIn, Twitter, etc.)        │
│ - AI suggestion engine (GitHub Models)              │
│ - Word count validation & optimization              │
│ - User authentication & preferences                 │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ Data & Integration Layer                            │
│ - Platform adapters (LinkedIn API, Twitter API)     │
│ - Database (SQLite → PostgreSQL)                    │
│ - Cache (Redis, optional)                           │
└─────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|----------|
| **Framework** | FastAPI | Modern, async-first web framework |
| **AI Models** | GitHub Models (GPT-4.1-mini) | Free-tier AI with Azure AI Inference SDK |
| **Database** | SQLite → PostgreSQL | SQLite for dev, PostgreSQL for production |
| **Auth** | OAuth 2.0 | Platform-native authentication |
| **Cache** | Redis (optional) | Session management & rate limiting |
| **Containers** | Docker + Docker Compose | Reproducible, cloud-agnostic deployment |
| **Testing** | pytest + pytest-asyncio | Unit, integration, and E2E tests |

---

## 🧪 Testing

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_suggestions.py -v

# Run with live output
pytest -s tests/
```

**Test Coverage Goals:**
- Unit tests: 70%+ coverage
- Integration tests: All API endpoints
- Performance tests: <2s p95 latency

---

## 🚢 Deployment

### Docker (Recommended)

```bash
# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Cloud Deployment

**AWS Lambda + API Gateway:**

```bash
# Install Mangum for AWS Lambda
pip install mangum

# Deploy with AWS SAM or Serverless Framework
# See docs/deployment/aws-lambda.md
```

**Heroku:**

```bash
heroku create trendresponse-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

**Azure Container Apps:**

```bash
az containerapp up \
  --name trendresponse \
  --resource-group myResourceGroup \
  --image trendresponse:latest \
  --target-port 8000
```

---

## 📖 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/linkedin/callback` | LinkedIn OAuth callback |
| POST | `/auth/logout` | Logout user |
| GET | `/auth/status` | Check auth status |

### Feed Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/feed/trending` | Get trending posts (limit=50) |
| GET | `/feed/posts/{post_id}` | Get full post details |

### Comment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/comments/validate` | Validate word count |
| POST | `/comments/suggest` | Generate AI suggestions |
| POST | `/comments/post` | Post comment to platform |
| GET | `/comments/history` | Get user's comment history |

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user/profile` | Get user profile |
| GET | `/user/preferences` | Get user preferences |
| PUT | `/user/preferences` | Update preferences |

---

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=sqlite+aiosqlite:///./trendresponse.db

# AI Models (GitHub Models - Free Tier)
GITHUB_TOKEN=ghp_your_token_here
MODEL_ENDPOINT=https://models.github.ai/inference/
MODEL_NAME=openai/gpt-4.1-mini

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret

# Security
SECRET_KEY=your-secret-key-change-in-production

# Comment Constraints
MIN_WORD_COUNT=10
MAX_WORD_COUNT=25
```

---

## 🗺️ Roadmap

### v0.1 - MVP ✅ (Current)
- [x] User authentication (LinkedIn OAuth stub)
- [x] AI-powered comment suggestions (GitHub Models)
- [x] Word count validation (10-25 words)
- [x] Basic API endpoints
- [x] Docker containerization

### v0.2 - Enhancement (Weeks 5-8)
- [ ] Full LinkedIn API integration
- [ ] Trending topic detection
- [ ] Batch comment operations
- [ ] Comment history analytics
- [ ] Redis caching layer

### v1.0 - Multi-Platform (Weeks 9-12)
- [ ] Twitter/X integration
- [ ] Reddit integration
- [ ] Advanced AI fine-tuning
- [ ] Team collaboration features
- [ ] Mobile-responsive web UI

### v1.5+ - Scale & Optimize
- [ ] Native iOS/Android apps
- [ ] Mastodon, Bluesky support
- [ ] Engagement analytics dashboard
- [ ] Enterprise tier (audit logs, team management)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'feat: add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Standards

- **Code style**: Black (line length: 100), isort, ruff
- **Testing**: pytest with 70%+ coverage
- **Commits**: Conventional Commits format
- **Documentation**: Docstrings for all public functions

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **GitHub Models**: Free AI model access for rapid development
- **FastAPI**: Modern, fast web framework for Python
- **Azure AI Inference SDK**: Seamless integration with GitHub models
- **LinkedIn & Twitter**: Social media platforms enabling engagement

---

## 📧 Contact

**Tim Dickey** - [@tim-dickey](https://github.com/tim-dickey)

**Project Link**: [https://github.com/tim-dickey/trendresponse](https://github.com/tim-dickey/trendresponse)

---

<div align="center">

**Built with ❤️ using GitHub Models and FastAPI**

</div>
