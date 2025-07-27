# 🚀 AI Pitch Deck Generator

**Professional AI-powered startup pitch deck creation platform**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9+-blue.svg)](https://typescriptlang.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

The AI Pitch Deck Generator is a comprehensive SaaS platform that automatically creates professional pitch decks for startups using advanced AI models. It combines market research, financial modeling, and content generation to produce investor-ready presentations.

## ✨ Features

### 🤖 AI-Powered Content Generation
- **Industry-specific content** tailored to your startup's sector
- **Dynamic storytelling** with compelling narratives
- **Competitor analysis** and market positioning
- **Professional slide layouts** with automated design

### 📊 Market Research Integration
- **Real-time market data** collection and analysis
- **TAM/SAM/SOM calculations** for market sizing
- **Competitor tracking** and competitive landscape analysis
- **Industry trends** and growth projections

### 💰 Financial Modeling Engine
- **Revenue projections** with multiple scenarios
- **Unit economics** analysis (LTV/CAC, payback period)
- **Valuation modeling** using industry-standard methods
- **Financial metrics** and KPIs

### 📄 Multi-Format Export System
- **Microsoft PowerPoint** (.pptx) with animations
- **PDF documents** for print and sharing
- **Google Slides** for cloud collaboration
- **Interactive web presentations** with embedded analytics

### 🏢 Enterprise Features
- **White-label solutions** for agencies and consultancies
- **SSO authentication** and role-based access
- **Advanced analytics** dashboard
- **CRM integration** (Salesforce, HubSpot)
- **API access** for developers
- **Bulk generation** capabilities

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Background    │              │
         │              │   Tasks         │              │
         │              │   (Celery)      │              │
         │              └─────────────────┘              │
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Cache       │              │
         │              │    (Redis)      │              │
         │              └─────────────────┘              │
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Monitoring    │              │
         │              │ (Prometheus)    │              │
         │              └─────────────────┘              │
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Reverse       │              │
         │              │    Proxy        │              │
         │              │   (Nginx)       │              │
         │              └─────────────────┘              │
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/hridaygupta/ai-pitchdeck-generator.git
cd ai-pitchdeck-generator
```

### 2. Quick Demo (No Setup Required)
```bash
# Start the demo server
cd backend
python3 -m uvicorn test_server:app --host 0.0.0.0 --port 8000 --reload

# Test the API
python3 ../test_api.py

# Run the demonstration
python3 ../demo.py
```

### 3. Generate Your First Pitch Deck
```bash
# Using the interactive script
python3 generate_pitch_deck.py

# Or using curl
curl -X POST "http://localhost:8000/api/generate-pitch-deck" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Startup",
    "industry": "SaaS",
    "problem_statement": "Describe the problem you solve",
    "solution_description": "Describe your solution",
    "target_market": "Who you target",
    "current_revenue": 50000,
    "team_size": 5
  }'
```

### 4. Full Production Deployment
```bash
# Copy environment variables
cp env.example .env

# Edit .env with your API keys and configuration
nano .env

# Start all services
docker-compose up -d

# Access the platform
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Documentation: http://localhost:8000/docs
```

## 📚 API Documentation

### Interactive Documentation
Visit `http://localhost:8000/docs` for the complete interactive API documentation.

### Key Endpoints

#### Generate Pitch Deck
```http
POST /api/generate-pitch-deck
Content-Type: application/json

{
  "name": "Startup Name",
  "industry": "Industry",
  "problem_statement": "Problem description",
  "solution_description": "Solution description",
  "target_market": "Target market",
  "current_revenue": 50000,
  "team_size": 5
}
```

#### Get Templates
```http
GET /api/templates
```

#### Get Export Formats
```http
GET /api/export/formats
```

#### Health Check
```http
GET /health
```

## 🎨 Available Templates

- **SaaS Startup Template** - 12 slides, modern design
- **Fintech Startup Template** - 15 slides, professional layout
- **Healthcare Startup Template** - 14 slides, medical focus
- **E-commerce Startup Template** - 13 slides, retail optimized
- **AI/ML Startup Template** - 16 slides, tech-focused

## 📊 Generated Content

Each pitch deck includes:

1. **Title Slide** - Company branding and tagline
2. **Problem Statement** - Market pain points and opportunities
3. **Solution Overview** - Product/service description
4. **Market Opportunity** - TAM/SAM/SOM analysis
5. **Business Model** - Revenue streams and pricing
6. **Traction & Metrics** - Growth indicators and KPIs
7. **Team** - Key personnel and expertise
8. **Financial Projections** - Revenue and growth forecasts
9. **Funding Ask** - Investment requirements and use of funds

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/pitchdeck

# Redis
REDIS_URL=redis://localhost:6379

# AI APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Security
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# File Storage
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📈 Monitoring

The platform includes comprehensive monitoring:

- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **Structured logging** - Application logs
- **Health checks** - Service monitoring

## 🔒 Security Features

- **JWT Authentication** - Secure API access
- **Rate Limiting** - API abuse prevention
- **CORS Protection** - Cross-origin security
- **Input Validation** - Data sanitization
- **SQL Injection Protection** - Database security

## 🧪 Testing

```bash
# Run API tests
python3 test_api.py

# Run comprehensive tests
python3 -m pytest tests/

# Run with coverage
python3 -m pytest --cov=src tests/
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Issues**: [GitHub Issues](https://github.com/hridaygupta/ai-pitchdeck-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hridaygupta/ai-pitchdeck-generator/discussions)

## 🚀 Roadmap

- [ ] **Advanced AI Models** - GPT-4, Claude, and custom fine-tuned models
- [ ] **Real-time Collaboration** - Multi-user editing and commenting
- [ ] **Advanced Analytics** - Pitch deck performance tracking
- [ ] **Mobile App** - iOS and Android applications
- [ ] **Integration APIs** - CRM, marketing automation, and analytics tools
- [ ] **White-label Platform** - Custom branding and domain support
- [ ] **Enterprise SSO** - SAML, OAuth, and LDAP integration
- [ ] **Advanced Export** - Video presentations and interactive demos

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework
- **React** - Frontend library
- **OpenAI** - AI content generation
- **Anthropic** - Advanced language models
- **PostgreSQL** - Reliable database
- **Redis** - High-performance caching
- **Docker** - Containerization platform

---

**Built with ❤️ for entrepreneurs and startups worldwide**

[![GitHub stars](https://img.shields.io/github/stars/hridaygupta/ai-pitchdeck-generator?style=social)](https://github.com/hridaygupta/ai-pitchdeck-generator)
[![GitHub forks](https://img.shields.io/github/forks/hridaygupta/ai-pitchdeck-generator?style=social)](https://github.com/hridaygupta/ai-pitchdeck-generator)
[![GitHub issues](https://img.shields.io/github/issues/hridaygupta/ai-pitchdeck-generator)](https://github.com/hridaygupta/ai-pitchdeck-generator/issues) 