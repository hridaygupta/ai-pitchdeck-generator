"""
API routes for pitch deck templates
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
router = APIRouter(prefix="/templates", tags=["templates"])

class TemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    industry: str
    slide_count: int
    preview_url: str
    is_premium: bool

@router.get("/", response_model=List[TemplateResponse])
async def get_templates(
    industry: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available pitch deck templates"""
    try:
        logger.info("Fetching templates", user_id=str(current_user.id), industry=industry)
        
        # This would query the database for templates
        # For now, return sample templates
        templates = [
            {
                "id": "template_1",
                "name": "SaaS Startup Template",
                "description": "Professional template for SaaS startups",
                "industry": "saas",
                "slide_count": 12,
                "preview_url": "/templates/saas/preview",
                "is_premium": False
            },
            {
                "id": "template_2",
                "name": "Fintech Startup Template",
                "description": "Comprehensive template for fintech companies",
                "industry": "fintech",
                "slide_count": 15,
                "preview_url": "/templates/fintech/preview",
                "is_premium": True
            },
            {
                "id": "template_3",
                "name": "Healthcare Startup Template",
                "description": "Specialized template for healthcare startups",
                "industry": "healthcare",
                "slide_count": 14,
                "preview_url": "/templates/healthcare/preview",
                "is_premium": False
            }
        ]
        
        # Filter by industry if specified
        if industry:
            templates = [t for t in templates if t["industry"] == industry]
        
        logger.info("Templates fetched successfully", count=len(templates))
        return templates
        
    except Exception as e:
        logger.error("Failed to fetch templates", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch templates"
        )

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific template details"""
    try:
        logger.info("Fetching template", template_id=template_id, user_id=str(current_user.id))
        
        # This would query the database for the specific template
        # For now, return a sample template
        template = {
            "id": template_id,
            "name": "Sample Template",
            "description": "Sample template description",
            "industry": "technology",
            "slide_count": 12,
            "preview_url": f"/templates/{template_id}/preview",
            "is_premium": False
        }
        
        logger.info("Template fetched successfully", template_id=template_id)
        return template
        
    except Exception as e:
        logger.error("Failed to fetch template", template_id=template_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch template"
        )

@router.post("/{template_id}/apply")
async def apply_template(
    template_id: str,
    startup_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Apply a template to a startup's pitch deck"""
    try:
        logger.info("Applying template", template_id=template_id, startup_id=startup_id, user_id=str(current_user.id))
        
        # This would apply the template to the startup's pitch deck
        # For now, return a success response
        result = {
            "status": "success",
            "template_id": template_id,
            "startup_id": startup_id,
            "slides_created": 12
        }
        
        logger.info("Template applied successfully", template_id=template_id, startup_id=startup_id)
        return result
        
    except Exception as e:
        logger.error("Failed to apply template", template_id=template_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to apply template"
        )

# Import already added above 