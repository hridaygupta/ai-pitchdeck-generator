from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import structlog
from datetime import datetime

from ...models.startup import Startup, IndustryType, FundingStage, RevenueModel
from ...models.slide import SlideType
from ...models.user import User
from ...ai.content_generator import ContentGenerator
from ...ai.market_researcher import MarketResearcher
from ...ai.financial_modeler import FinancialModeler
from ...services.template_engine import TemplateEngine
from ...database.connection import get_db
from ...utils.auth import get_current_user

logger = structlog.get_logger()
router = APIRouter()

# Pydantic models for request/response
class StartupCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    tagline: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    website: Optional[str] = None
    industry: IndustryType
    funding_stage: FundingStage
    revenue_model: RevenueModel
    problem_statement: Optional[str] = None
    solution_description: Optional[str] = None
    unique_value_proposition: Optional[str] = None
    target_market: Optional[str] = None
    team_size: Optional[int] = Field(None, ge=1)
    customer_count: Optional[int] = Field(None, ge=0)
    current_revenue: Optional[float] = Field(None, ge=0)
    funding_ask: Optional[float] = Field(None, ge=0)

class PitchDeckGenerationRequest(BaseModel):
    startup_id: str
    slide_types: Optional[List[SlideType]] = None
    template_preference: Optional[str] = "classic"
    include_market_research: bool = True
    include_financial_modeling: bool = True
    custom_prompts: Optional[Dict[str, str]] = None

class GenerationResponse(BaseModel):
    pitch_deck_id: str
    status: str
    estimated_completion_time: Optional[int] = None
    progress: Optional[Dict[str, Any]] = None

class GenerationStatusResponse(BaseModel):
    pitch_deck_id: str
    status: str
    progress: Dict[str, Any]
    completed_slides: List[Dict[str, Any]]
    errors: List[str]

# Initialize services
content_generator = ContentGenerator()
market_researcher = MarketResearcher()
financial_modeler = FinancialModeler()
template_engine = TemplateEngine()

@router.post("/startup", response_model=Dict[str, Any])
async def create_startup(
    request: StartupCreateRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a new startup profile"""
    try:
        db = get_db()
        
        # Check if user can create more startups
        if not current_user.can_create_pitch_deck():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have reached the limit for creating pitch decks. Please upgrade your plan."
            )
        
        # Create startup
        startup = Startup(
            name=request.name,
            tagline=request.tagline,
            description=request.description,
            website=request.website,
            industry=request.industry,
            funding_stage=request.funding_stage,
            revenue_model=request.revenue_model,
            problem_statement=request.problem_statement,
            solution_description=request.solution_description,
            unique_value_proposition=request.unique_value_proposition,
            target_market=request.target_market,
            team_size=request.team_size,
            customer_count=request.customer_count,
            current_revenue=request.current_revenue,
            funding_ask=request.funding_ask,
            user_id=current_user.id
        )
        
        db.add(startup)
        db.commit()
        db.refresh(startup)
        
        # Increment user's pitch deck count
        current_user.increment_pitch_decks()
        db.commit()
        
        logger.info("Startup created successfully", startup_id=str(startup.id), user_id=str(current_user.id))
        
        return {
            "startup": startup.to_dict(),
            "message": "Startup created successfully"
        }
        
    except Exception as e:
        logger.error("Failed to create startup", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create startup"
        )

@router.post("/pitch-deck", response_model=GenerationResponse)
async def generate_pitch_deck(
    request: PitchDeckGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Generate a complete pitch deck for a startup"""
    try:
        db = get_db()
        
        # Check if user can use AI generation
        if not current_user.can_use_ai_generation():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have reached the limit for AI generations. Please upgrade your plan."
            )
        
        # Get startup
        startup = db.query(Startup).filter(
            Startup.id == request.startup_id,
            Startup.user_id == current_user.id
        ).first()
        
        if not startup:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Startup not found"
            )
        
        # Create pitch deck
        from ...models.pitch_deck import PitchDeck, PitchDeckStatus, PitchDeckTemplate
        
        pitch_deck = PitchDeck(
            title=f"{startup.name} - Pitch Deck",
            description=f"AI-generated pitch deck for {startup.name}",
            template=PitchDeckTemplate(request.template_preference),
            startup_id=startup.id,
            user_id=current_user.id,
            status=PitchDeckStatus.GENERATING,
            generation_settings={
                "slide_types": [st.value for st in (request.slide_types or [])],
                "include_market_research": request.include_market_research,
                "include_financial_modeling": request.include_financial_modeling,
                "custom_prompts": request.custom_prompts
            }
        )
        
        db.add(pitch_deck)
        db.commit()
        db.refresh(pitch_deck)
        
        # Add background task for generation
        background_tasks.add_task(
            generate_pitch_deck_background,
            pitch_deck.id,
            startup.id,
            request,
            current_user.id
        )
        
        # Increment user's generation count
        current_user.increment_generations()
        db.commit()
        
        logger.info("Pitch deck generation started", 
                   pitch_deck_id=str(pitch_deck.id), 
                   startup_id=str(startup.id))
        
        return GenerationResponse(
            pitch_deck_id=str(pitch_deck.id),
            status="generating",
            estimated_completion_time=300  # 5 minutes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to start pitch deck generation", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start pitch deck generation"
        )

@router.get("/pitch-deck/{pitch_deck_id}/status", response_model=GenerationStatusResponse)
async def get_generation_status(
    pitch_deck_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get the status of pitch deck generation"""
    try:
        db = get_db()
        
        pitch_deck = db.query(PitchDeck).filter(
            PitchDeck.id == pitch_deck_id,
            PitchDeck.user_id == current_user.id
        ).first()
        
        if not pitch_deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pitch deck not found"
            )
        
        # Get slides
        slides = db.query(Slide).filter(
            Slide.pitch_deck_id == pitch_deck.id
        ).order_by(Slide.order).all()
        
        completed_slides = [slide.to_dict() for slide in slides]
        
        return GenerationStatusResponse(
            pitch_deck_id=str(pitch_deck.id),
            status=pitch_deck.status.value,
            progress={
                "total_slides": len(completed_slides),
                "completed_slides": len(completed_slides),
                "estimated_remaining_time": 0 if pitch_deck.status.value == "completed" else 60
            },
            completed_slides=completed_slides,
            errors=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get generation status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get generation status"
        )

@router.post("/slide/{slide_type}")
async def generate_single_slide(
    slide_type: SlideType,
    startup_id: str,
    custom_prompt: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Generate content for a single slide"""
    try:
        db = get_db()
        
        # Check if user can use AI generation
        if not current_user.can_use_ai_generation():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have reached the limit for AI generations. Please upgrade your plan."
            )
        
        # Get startup
        startup = db.query(Startup).filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id
        ).first()
        
        if not startup:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Startup not found"
            )
        
        # Generate slide content
        slide_content = await content_generator.generate_slide_content(startup, slide_type)
        
        # Increment user's generation count
        current_user.increment_generations()
        db.commit()
        
        logger.info("Single slide generated", 
                   slide_type=slide_type.value, 
                   startup_id=str(startup.id))
        
        return {
            "slide_content": slide_content,
            "message": f"{slide_type.value.replace('_', ' ').title()} slide generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to generate single slide", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate slide content"
        )

@router.post("/market-research/{startup_id}")
async def generate_market_research(
    startup_id: str,
    current_user: User = Depends(get_current_user)
):
    """Generate comprehensive market research for a startup"""
    try:
        db = get_db()
        
        # Check if user can use AI generation
        if not current_user.can_use_ai_generation():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have reached the limit for AI generations. Please upgrade your plan."
            )
        
        # Get startup
        startup = db.query(Startup).filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id
        ).first()
        
        if not startup:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Startup not found"
            )
        
        # Generate market research
        market_research = await market_researcher.generate_market_research(startup)
        
        # Update startup with market research data
        startup.market_size_tam = market_research.get("tam")
        startup.market_size_sam = market_research.get("sam")
        startup.market_size_som = market_research.get("som")
        startup.market_growth_rate = market_research.get("growth_rate")
        startup.competitors = market_research.get("competitors")
        
        db.commit()
        
        # Increment user's generation count
        current_user.increment_generations()
        db.commit()
        
        logger.info("Market research generated", startup_id=str(startup.id))
        
        return {
            "market_research": market_research,
            "message": "Market research generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to generate market research", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate market research"
        )

@router.post("/financial-model/{startup_id}")
async def generate_financial_model(
    startup_id: str,
    current_user: User = Depends(get_current_user)
):
    """Generate financial projections and model for a startup"""
    try:
        db = get_db()
        
        # Check if user can use AI generation
        if not current_user.can_use_ai_generation():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have reached the limit for AI generations. Please upgrade your plan."
            )
        
        # Get startup
        startup = db.query(Startup).filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id
        ).first()
        
        if not startup:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Startup not found"
            )
        
        # Generate financial model
        financial_model = await financial_modeler.generate_financial_model(startup)
        
        # Update startup with financial data
        startup.financial_projections = financial_model.get("projections")
        startup.unit_economics = financial_model.get("unit_economics")
        startup.burn_rate = financial_model.get("burn_rate")
        startup.runway_months = financial_model.get("runway_months")
        
        db.commit()
        
        # Increment user's generation count
        current_user.increment_generations()
        db.commit()
        
        logger.info("Financial model generated", startup_id=str(startup.id))
        
        return {
            "financial_model": financial_model,
            "message": "Financial model generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to generate financial model", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate financial model"
        )

async def generate_pitch_deck_background(
    pitch_deck_id: str,
    startup_id: str,
    request: PitchDeckGenerationRequest,
    user_id: str
):
    """Background task for generating pitch deck content"""
    try:
        db = get_db()
        
        # Get startup and pitch deck
        startup = db.query(Startup).filter(Startup.id == startup_id).first()
        pitch_deck = db.query(PitchDeck).filter(PitchDeck.id == pitch_deck_id).first()
        
        if not startup or not pitch_deck:
            logger.error("Startup or pitch deck not found for background generation")
            return
        
        # Update status
        pitch_deck.status = PitchDeckStatus.GENERATING
        db.commit()
        
        # Generate market research if requested
        if request.include_market_research:
            try:
                market_research = await market_researcher.generate_market_research(startup)
                startup.market_size_tam = market_research.get("tam")
                startup.market_size_sam = market_research.get("sam")
                startup.market_size_som = market_research.get("som")
                startup.market_growth_rate = market_research.get("growth_rate")
                startup.competitors = market_research.get("competitors")
                db.commit()
            except Exception as e:
                logger.error("Failed to generate market research", error=str(e))
        
        # Generate financial model if requested
        if request.include_financial_modeling:
            try:
                financial_model = await financial_modeler.generate_financial_model(startup)
                startup.financial_projections = financial_model.get("projections")
                startup.unit_economics = financial_model.get("unit_economics")
                startup.burn_rate = financial_model.get("burn_rate")
                startup.runway_months = financial_model.get("runway_months")
                db.commit()
            except Exception as e:
                logger.error("Failed to generate financial model", error=str(e))
        
        # Generate slide content
        slide_types = request.slide_types or [
            SlideType.TITLE,
            SlideType.PROBLEM,
            SlideType.SOLUTION,
            SlideType.MARKET_OPPORTUNITY,
            SlideType.BUSINESS_MODEL,
            SlideType.TRACTION,
            SlideType.COMPETITION,
            SlideType.TEAM,
            SlideType.FINANCIALS,
            SlideType.FUNDING_ASK
        ]
        
        slides_content = await content_generator.generate_pitch_deck_content(startup, slide_types)
        
        # Create slides
        for i, slide_content in enumerate(slides_content):
            slide = Slide(
                title=slide_content["content"]["title"],
                slide_type=SlideType(slide_content["slide_type"]),
                content=slide_content["content"],
                order=i + 1,
                pitch_deck_id=pitch_deck.id,
                ai_generated=True,
                generation_model=slide_content["model_used"],
                status=SlideStatus.COMPLETED
            )
            db.add(slide)
        
        # Update pitch deck
        pitch_deck.status = PitchDeckStatus.COMPLETED
        pitch_deck.generated_at = datetime.utcnow()
        pitch_deck.total_slides = len(slides_content)
        db.commit()
        
        logger.info("Pitch deck generation completed", 
                   pitch_deck_id=str(pitch_deck.id), 
                   slides_count=len(slides_content))
        
    except Exception as e:
        logger.error("Background pitch deck generation failed", error=str(e))
        # Update status to failed
        try:
            pitch_deck.status = PitchDeckStatus.DRAFT
            db.commit()
        except:
            pass 