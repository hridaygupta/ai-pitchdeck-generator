from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from typing import Optional, List, Dict, Any

from ..database.connection import Base

class SlideType(enum.Enum):
    """Types of slides in a pitch deck"""
    TITLE = "title"
    PROBLEM = "problem"
    SOLUTION = "solution"
    MARKET_OPPORTUNITY = "market_opportunity"
    BUSINESS_MODEL = "business_model"
    TRACTION = "traction"
    COMPETITION = "competition"
    TEAM = "team"
    FINANCIALS = "financials"
    FUNDING_ASK = "funding_ask"
    ROADMAP = "roadmap"
    CONTACT = "contact"
    CUSTOM = "custom"

class SlideLayout(enum.Enum):
    """Slide layout types"""
    TITLE_CENTER = "title_center"
    TITLE_SUBTITLE = "title_subtitle"
    BULLET_POINTS = "bullet_points"
    TWO_COLUMN = "two_column"
    THREE_COLUMN = "three_column"
    GRID = "grid"
    CHART = "chart"
    IMAGE_CENTER = "image_center"
    SPLIT_SCREEN = "split_screen"
    TIMELINE = "timeline"
    COMPARISON = "comparison"
    CUSTOM = "custom"

class SlideStatus(enum.Enum):
    """Status of slide generation"""
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    REVIEWED = "reviewed"
    APPROVED = "approved"

class Slide(Base):
    """Slide model for storing individual slides within pitch decks"""
    __tablename__ = "slides"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    title = Column(String(255), nullable=False)
    subtitle = Column(String(500))
    slide_type = Column(Enum(SlideType), nullable=False, index=True)
    layout = Column(Enum(SlideLayout), default=SlideLayout.TITLE_SUBTITLE)
    
    # Content
    content = Column(JSON)  # Main content structure
    text_content = Column(Text)  # Plain text content
    bullet_points = Column(JSON)  # Array of bullet points
    key_metrics = Column(JSON)  # Important numbers and metrics
    
    # Visual elements
    images = Column(JSON)  # Array of image URLs and metadata
    charts = Column(JSON)  # Chart data and configuration
    icons = Column(JSON)  # Icon references and positioning
    colors = Column(JSON)  # Color scheme for this slide
    
    # Design and styling
    design_config = Column(JSON)  # Fonts, spacing, alignment
    animations = Column(JSON)  # Animation settings
    transitions = Column(JSON)  # Transition effects
    
    # AI generation
    ai_generated = Column(Boolean, default=True)
    generation_prompt = Column(Text)  # Original prompt used
    generation_model = Column(String(100))  # AI model used
    generation_settings = Column(JSON)  # Generation parameters
    
    # Status and metadata
    status = Column(Enum(SlideStatus), default=SlideStatus.DRAFT)
    order = Column(Integer, nullable=False)  # Position in deck
    estimated_duration = Column(Integer)  # Time to present this slide
    
    # Version control
    version = Column(String(50), default="1.0")
    parent_slide_id = Column(UUID(as_uuid=True), ForeignKey("slides.id"))
    version_history = Column(JSON)  # Array of previous versions
    
    # Analytics
    view_count = Column(Integer, default=0)
    edit_count = Column(Integer, default=0)
    feedback_score = Column(Float)
    feedback_comments = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    generated_at = Column(DateTime)
    reviewed_at = Column(DateTime)
    
    # Relationships
    pitch_deck_id = Column(UUID(as_uuid=True), ForeignKey("pitch_decks.id"), nullable=False)
    pitch_deck = relationship("PitchDeck", back_populates="slides")
    
    def __repr__(self):
        return f"<Slide(id={self.id}, title='{self.title}', type={self.slide_type}, order={self.order})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert slide to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "subtitle": self.subtitle,
            "slide_type": self.slide_type.value if self.slide_type else None,
            "layout": self.layout.value if self.layout else None,
            "content": self.content,
            "text_content": self.text_content,
            "bullet_points": self.bullet_points,
            "key_metrics": self.key_metrics,
            "images": self.images,
            "charts": self.charts,
            "icons": self.icons,
            "colors": self.colors,
            "design_config": self.design_config,
            "animations": self.animations,
            "transitions": self.transitions,
            "ai_generated": self.ai_generated,
            "generation_prompt": self.generation_prompt,
            "generation_model": self.generation_model,
            "generation_settings": self.generation_settings,
            "status": self.status.value if self.status else None,
            "order": self.order,
            "estimated_duration": self.estimated_duration,
            "version": self.version,
            "parent_slide_id": str(self.parent_slide_id) if self.parent_slide_id else None,
            "version_history": self.version_history,
            "view_count": self.view_count,
            "edit_count": self.edit_count,
            "feedback_score": self.feedback_score,
            "feedback_comments": self.feedback_comments,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "pitch_deck_id": str(self.pitch_deck_id)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Slide":
        """Create slide from dictionary"""
        # Convert enum values
        if "slide_type" in data and data["slide_type"]:
            data["slide_type"] = SlideType(data["slide_type"])
        if "layout" in data and data["layout"]:
            data["layout"] = SlideLayout(data["layout"])
        if "status" in data and data["status"]:
            data["status"] = SlideStatus(data["status"])
        
        return cls(**data)
    
    def duplicate(self) -> "Slide":
        """Create a duplicate of the slide"""
        new_slide = Slide(
            title=f"{self.title} (Copy)",
            subtitle=self.subtitle,
            slide_type=self.slide_type,
            layout=self.layout,
            content=self.content.copy() if self.content else None,
            text_content=self.text_content,
            bullet_points=self.bullet_points.copy() if self.bullet_points else None,
            key_metrics=self.key_metrics.copy() if self.key_metrics else None,
            images=self.images.copy() if self.images else None,
            charts=self.charts.copy() if self.charts else None,
            icons=self.icons.copy() if self.icons else None,
            colors=self.colors.copy() if self.colors else None,
            design_config=self.design_config.copy() if self.design_config else None,
            animations=self.animations.copy() if self.animations else None,
            transitions=self.transitions.copy() if self.transitions else None,
            ai_generated=self.ai_generated,
            generation_prompt=self.generation_prompt,
            generation_model=self.generation_model,
            generation_settings=self.generation_settings.copy() if self.generation_settings else None,
            status=SlideStatus.DRAFT,
            estimated_duration=self.estimated_duration,
            parent_slide_id=self.id
        )
        
        return new_slide
    
    def update_content(self, new_content: Dict[str, Any]) -> None:
        """Update slide content"""
        self.content = new_content
        self.updated_at = func.now()
        self.edit_count += 1
    
    def add_bullet_point(self, bullet_point: str) -> None:
        """Add a bullet point to the slide"""
        if not self.bullet_points:
            self.bullet_points = []
        self.bullet_points.append(bullet_point)
        self.updated_at = func.now()
        self.edit_count += 1
    
    def remove_bullet_point(self, index: int) -> bool:
        """Remove a bullet point by index"""
        if self.bullet_points and 0 <= index < len(self.bullet_points):
            self.bullet_points.pop(index)
            self.updated_at = func.now()
            self.edit_count += 1
            return True
        return False
    
    def add_key_metric(self, metric_name: str, value: Any, unit: str = None) -> None:
        """Add a key metric to the slide"""
        if not self.key_metrics:
            self.key_metrics = []
        
        metric = {
            "name": metric_name,
            "value": value,
            "unit": unit
        }
        self.key_metrics.append(metric)
        self.updated_at = func.now()
        self.edit_count += 1
    
    def add_image(self, image_url: str, alt_text: str = None, position: Dict[str, Any] = None) -> None:
        """Add an image to the slide"""
        if not self.images:
            self.images = []
        
        image = {
            "url": image_url,
            "alt_text": alt_text,
            "position": position or {"x": 0, "y": 0, "width": 100, "height": 100}
        }
        self.images.append(image)
        self.updated_at = func.now()
        self.edit_count += 1
    
    def add_chart(self, chart_type: str, data: Dict[str, Any], config: Dict[str, Any] = None) -> None:
        """Add a chart to the slide"""
        if not self.charts:
            self.charts = []
        
        chart = {
            "type": chart_type,
            "data": data,
            "config": config or {}
        }
        self.charts.append(chart)
        self.updated_at = func.now()
        self.edit_count += 1
    
    def get_content_summary(self) -> str:
        """Get a summary of the slide content"""
        summary_parts = []
        
        if self.title:
            summary_parts.append(f"Title: {self.title}")
        
        if self.subtitle:
            summary_parts.append(f"Subtitle: {self.subtitle}")
        
        if self.text_content:
            summary_parts.append(f"Content: {self.text_content[:100]}...")
        
        if self.bullet_points:
            summary_parts.append(f"Bullet points: {len(self.bullet_points)} items")
        
        if self.key_metrics:
            summary_parts.append(f"Key metrics: {len(self.key_metrics)} items")
        
        return " | ".join(summary_parts)
    
    def validate_content(self) -> List[str]:
        """Validate slide content and return list of issues"""
        issues = []
        
        if not self.title:
            issues.append("Slide title is required")
        
        if not self.content and not self.text_content and not self.bullet_points:
            issues.append("Slide must have some content")
        
        if self.order < 1:
            issues.append("Slide order must be positive")
        
        return issues 