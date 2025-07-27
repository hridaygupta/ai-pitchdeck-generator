"""
API routes for pitch deck analysis
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from pydantic import BaseModel
import structlog

from ...models.user import User
from ...database.connection import get_db
from ...utils.auth import get_current_user
from sqlalchemy.orm import Session

logger = structlog.get_logger()
router = APIRouter(prefix="/analysis", tags=["analysis"])

class AnalysisRequest(BaseModel):
    pitch_deck_id: str
    analysis_type: str  # "content", "design", "financial", "comprehensive"

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    score: float
    insights: List[str]
    recommendations: List[str]

@router.post("/", response_model=AnalysisResponse)
async def analyze_pitch_deck(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze a pitch deck and provide insights"""
    try:
        logger.info("Starting pitch deck analysis", 
                   pitch_deck_id=request.pitch_deck_id, 
                   analysis_type=request.analysis_type,
                   user_id=str(current_user.id))
        
        # This would perform actual analysis
        # For now, return sample analysis results
        analysis_id = f"analysis_{request.pitch_deck_id}_{request.analysis_type}"
        
        result = {
            "analysis_id": analysis_id,
            "status": "completed",
            "score": 8.5,
            "insights": [
                "Strong problem statement with clear market validation",
                "Competitive analysis could be more comprehensive",
                "Financial projections are realistic and well-supported",
                "Team slide effectively highlights key expertise"
            ],
            "recommendations": [
                "Add more specific market size data",
                "Include customer testimonials or case studies",
                "Strengthen the competitive positioning",
                "Add more visual elements to improve engagement"
            ]
        }
        
        logger.info("Pitch deck analysis completed", analysis_id=analysis_id)
        return result
        
    except Exception as e:
        logger.error("Failed to analyze pitch deck", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze pitch deck"
        )

@router.get("/{analysis_id}")
async def get_analysis_results(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed analysis results"""
    try:
        logger.info("Fetching analysis results", analysis_id=analysis_id, user_id=str(current_user.id))
        
        # This would fetch actual analysis results
        # For now, return sample results
        results = {
            "analysis_id": analysis_id,
            "pitch_deck_id": "sample_deck_id",
            "analysis_type": "comprehensive",
            "created_at": "2024-07-26T10:00:00Z",
            "overall_score": 8.5,
            "sections": {
                "content": {
                    "score": 8.0,
                    "strengths": ["Clear value proposition", "Strong problem statement"],
                    "weaknesses": ["Limited market data", "Weak competitive analysis"]
                },
                "design": {
                    "score": 9.0,
                    "strengths": ["Professional layout", "Consistent branding"],
                    "weaknesses": ["Could use more visuals"]
                },
                "financial": {
                    "score": 8.5,
                    "strengths": ["Realistic projections", "Clear revenue model"],
                    "weaknesses": ["Missing unit economics"]
                }
            },
            "recommendations": [
                "Add more market research data",
                "Include customer testimonials",
                "Strengthen competitive positioning",
                "Add visual charts and graphs"
            ]
        }
        
        logger.info("Analysis results retrieved", analysis_id=analysis_id)
        return results
        
    except Exception as e:
        logger.error("Failed to get analysis results", analysis_id=analysis_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get analysis results"
        )

@router.get("/types")
async def get_analysis_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available analysis types"""
    try:
        logger.info("Fetching analysis types", user_id=str(current_user.id))
        
        analysis_types = [
            {
                "type": "content",
                "name": "Content Analysis",
                "description": "Analyze the quality and effectiveness of content",
                "duration": "2-3 minutes"
            },
            {
                "type": "design",
                "name": "Design Analysis",
                "description": "Evaluate visual design and presentation quality",
                "duration": "1-2 minutes"
            },
            {
                "type": "financial",
                "name": "Financial Analysis",
                "description": "Review financial projections and assumptions",
                "duration": "3-4 minutes"
            },
            {
                "type": "comprehensive",
                "name": "Comprehensive Analysis",
                "description": "Complete analysis of all aspects",
                "duration": "5-7 minutes"
            }
        ]
        
        logger.info("Analysis types fetched successfully", count=len(analysis_types))
        return analysis_types
        
    except Exception as e:
        logger.error("Failed to fetch analysis types", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch analysis types"
        )

# Import already added above 