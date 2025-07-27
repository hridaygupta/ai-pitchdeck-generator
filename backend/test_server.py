"""
Simple test server to demonstrate the AI Pitch Deck Generator
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import structlog
import os

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="AI Pitch Deck Generator",
    description="Professional AI-powered startup pitch deck creation platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class StartupRequest(BaseModel):
    name: str
    industry: str
    problem_statement: str
    solution_description: str
    target_market: str
    current_revenue: float = 0
    team_size: int = 1

class PitchDeckResponse(BaseModel):
    startup_name: str
    slides: List[Dict[str, Any]]
    market_data: Dict[str, Any]
    financial_model: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Pitch Deck Generator API",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "AI-powered content generation",
            "Market research integration",
            "Financial modeling",
            "Multi-format export",
            "Real-time collaboration"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-07-26T10:00:00Z",
        "services": {
            "api": "running",
            "ai_models": "available",
            "database": "not_required_for_demo"
        }
    }

@app.post("/api/generate-pitch-deck", response_model=PitchDeckResponse)
async def generate_pitch_deck(request: StartupRequest):
    """Generate a complete pitch deck for a startup"""
    try:
        logger.info("Generating pitch deck", startup_name=request.name, industry=request.industry)
        
        # Simulate AI content generation
        slides = [
            {
                "type": "title",
                "title": f"{request.name} - Pitch Deck",
                "subtitle": "Revolutionary solution for the future",
                "content": f"Welcome to {request.name}, a game-changing startup in the {request.industry} industry."
            },
            {
                "type": "problem",
                "title": "The Problem",
                "content": request.problem_statement,
                "bullet_points": [
                    "Market inefficiency",
                    "Customer pain points",
                    "Unmet needs"
                ]
            },
            {
                "type": "solution",
                "title": "Our Solution",
                "content": request.solution_description,
                "bullet_points": [
                    "Innovative approach",
                    "Scalable technology",
                    "Proven methodology"
                ]
            },
            {
                "type": "market_opportunity",
                "title": "Market Opportunity",
                "content": f"Targeting the {request.target_market} market",
                "metrics": {
                    "tam": 1000000000,
                    "sam": 150000000,
                    "som": 4500000
                }
            },
            {
                "type": "business_model",
                "title": "Business Model",
                "content": "Sustainable revenue model with multiple streams",
                "revenue_streams": [
                    "Subscription fees",
                    "Transaction fees",
                    "Data licensing"
                ]
            },
            {
                "type": "traction",
                "title": "Traction & Metrics",
                "content": "Strong growth and market validation",
                "metrics": {
                    "current_revenue": request.current_revenue,
                    "team_size": request.team_size,
                    "growth_rate": "25% month-over-month"
                }
            },
            {
                "type": "team",
                "title": "Our Team",
                "content": "Experienced team with deep industry expertise",
                "team_members": [
                    "CEO - Industry veteran",
                    "CTO - Technical expert",
                    "CMO - Growth specialist"
                ]
            },
            {
                "type": "financials",
                "title": "Financial Projections",
                "content": "Strong financial outlook with clear path to profitability",
                "projections": {
                    "year_1_revenue": request.current_revenue * 12,
                    "year_2_revenue": request.current_revenue * 24,
                    "year_3_revenue": request.current_revenue * 48
                }
            },
            {
                "type": "funding_ask",
                "title": "Funding Ask",
                "content": "Seeking strategic investment for growth",
                "funding_details": {
                    "amount": 2000000,
                    "use_of_funds": [
                        "Product development",
                        "Market expansion",
                        "Team growth"
                    ]
                }
            }
        ]
        
        # Simulate market research
        market_data = {
            "industry": request.industry,
            "market_size": {
                "tam": 1000000000,
                "sam": 150000000,
                "som": 4500000
            },
            "growth_rate": "12% annually",
            "key_players": [
                "Competitor A - Market leader",
                "Competitor B - Growing challenger",
                "Competitor C - Niche player"
            ],
            "trends": [
                "Digital transformation",
                "AI/ML integration",
                "Remote work adoption"
            ]
        }
        
        # Simulate financial model
        financial_model = {
            "revenue_projections": {
                "year_1": request.current_revenue * 12,
                "year_2": request.current_revenue * 24,
                "year_3": request.current_revenue * 48
            },
            "unit_economics": {
                "customer_acquisition_cost": 100,
                "customer_lifetime_value": 500,
                "ltv_cac_ratio": 5.0
            },
            "valuation": {
                "estimated_valuation": 10000000,
                "methodology": "Revenue multiple"
            }
        }
        
        logger.info("Pitch deck generated successfully", startup_name=request.name)
        
        return PitchDeckResponse(
            startup_name=request.name,
            slides=slides,
            market_data=market_data,
            financial_model=financial_model
        )
        
    except Exception as e:
        logger.error("Failed to generate pitch deck", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate pitch deck")

@app.get("/api/templates")
async def get_templates():
    """Get available pitch deck templates"""
    return [
        {
            "id": "saas",
            "name": "SaaS Startup Template",
            "description": "Professional template for SaaS startups",
            "slide_count": 12,
            "is_premium": False
        },
        {
            "id": "fintech",
            "name": "Fintech Startup Template",
            "description": "Comprehensive template for fintech companies",
            "slide_count": 15,
            "is_premium": True
        },
        {
            "id": "healthcare",
            "name": "Healthcare Startup Template",
            "description": "Specialized template for healthcare startups",
            "slide_count": 14,
            "is_premium": False
        }
    ]

@app.get("/api/export/formats")
async def get_export_formats():
    """Get available export formats"""
    return [
        {
            "format": "powerpoint",
            "name": "Microsoft PowerPoint",
            "extension": ".pptx",
            "description": "Professional presentation format"
        },
        {
            "format": "pdf",
            "name": "PDF Document",
            "extension": ".pdf",
            "description": "Portable document format"
        },
        {
            "format": "google_slides",
            "name": "Google Slides",
            "extension": ".gslides",
            "description": "Cloud-based presentation"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 