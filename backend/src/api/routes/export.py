"""
API routes for document export
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any
from pydantic import BaseModel
import structlog

from ...models.user import User
from ...database.connection import get_db
from ...utils.auth import get_current_user
from sqlalchemy.orm import Session

logger = structlog.get_logger()
router = APIRouter(prefix="/export", tags=["export"])

class ExportRequest(BaseModel):
    pitch_deck_id: str
    format: str  # "powerpoint", "pdf", "google_slides"
    include_notes: bool = False
    custom_styling: bool = True

class ExportResponse(BaseModel):
    task_id: str
    status: str
    estimated_completion: str

@router.post("/", response_model=ExportResponse)
async def export_pitch_deck(
    request: ExportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export pitch deck to various formats"""
    try:
        logger.info("Starting pitch deck export", 
                   pitch_deck_id=request.pitch_deck_id, 
                   format=request.format,
                   user_id=str(current_user.id))
        
        # This would start a background task for export
        # For now, return a placeholder response
        task_id = f"export_{request.pitch_deck_id}_{request.format}"
        
        result = {
            "task_id": task_id,
            "status": "processing",
            "estimated_completion": "5 minutes"
        }
        
        logger.info("Export task created", task_id=task_id)
        return result
        
    except Exception as e:
        logger.error("Failed to start export", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start export"
        )

@router.get("/status/{task_id}")
async def get_export_status(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get export task status"""
    try:
        logger.info("Checking export status", task_id=task_id, user_id=str(current_user.id))
        
        # This would check the actual task status
        # For now, return a sample status
        status_info = {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "download_url": f"/downloads/{task_id}.pptx",
            "file_size": "2.5MB"
        }
        
        logger.info("Export status retrieved", task_id=task_id)
        return status_info
        
    except Exception as e:
        logger.error("Failed to get export status", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get export status"
        )

@router.get("/formats")
async def get_export_formats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available export formats"""
    try:
        logger.info("Fetching export formats", user_id=str(current_user.id))
        
        formats = [
            {
                "format": "powerpoint",
                "name": "Microsoft PowerPoint",
                "extension": ".pptx",
                "description": "Professional presentation format",
                "is_available": True
            },
            {
                "format": "pdf",
                "name": "PDF Document",
                "extension": ".pdf",
                "description": "Portable document format",
                "is_available": True
            },
            {
                "format": "google_slides",
                "name": "Google Slides",
                "extension": ".gslides",
                "description": "Cloud-based presentation",
                "is_available": True
            }
        ]
        
        logger.info("Export formats fetched successfully", count=len(formats))
        return formats
        
    except Exception as e:
        logger.error("Failed to fetch export formats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch export formats"
        )

# Import already added above 