from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from typing import Optional, List, Dict, Any

from ..database.connection import Base

class PitchDeckStatus(enum.Enum):
    """Status of pitch deck generation"""
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class PitchDeckTemplate(enum.Enum):
    """Pitch deck template types"""
    CLASSIC = "classic"
    MODERN = "modern"
    MINIMAL = "minimal"
    CREATIVE = "creative"
    CORPORATE = "corporate"
    STARTUP = "startup"
    INVESTOR = "investor"
    CUSTOM = "custom"

class PitchDeck(Base):
    """Pitch deck model for storing pitch deck documents"""
    __tablename__ = "pitch_decks"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    title = Column(String(255), nullable=False)
    description = Column(Text)
    version = Column(String(50), default="1.0")
    
    # Template and design
    template = Column(Enum(PitchDeckTemplate), default=PitchDeckTemplate.CLASSIC)
    design_config = Column(JSON)  # Color scheme, fonts, layout preferences
    branding = Column(JSON)  # Logo, brand colors, company information
    
    # Content and structure
    slide_order = Column(JSON)  # Array of slide IDs in order
    total_slides = Column(Integer, default=0)
    estimated_duration = Column(Integer)  # Presentation duration in minutes
    
    # Generation settings
    generation_settings = Column(JSON)  # AI model preferences, content style
    industry_focus = Column(String(100))
    target_audience = Column(String(100))
    
    # Status and metadata
    status = Column(Enum(PitchDeckStatus), default=PitchDeckStatus.DRAFT)
    is_public = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    
    # Analytics and performance
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    feedback_score = Column(Float)
    feedback_comments = Column(JSON)
    
    # Export information
    export_formats = Column(JSON)  # Available export formats
    last_exported = Column(DateTime)
    export_settings = Column(JSON)  # Export preferences
    
    # Collaboration
    collaborators = Column(JSON)  # List of user IDs with access
    permissions = Column(JSON)  # Permission settings for collaborators
    
    # Version control
    parent_version_id = Column(UUID(as_uuid=True), ForeignKey("pitch_decks.id"))
    version_history = Column(JSON)  # Array of previous versions
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    generated_at = Column(DateTime)
    published_at = Column(DateTime)
    
    # Relationships
    startup_id = Column(UUID(as_uuid=True), ForeignKey("startups.id"), nullable=False)
    startup = relationship("Startup", back_populates="pitch_decks")
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="pitch_decks")
    
    # Slide relationship
    slides = relationship("Slide", back_populates="pitch_deck", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PitchDeck(id={self.id}, title='{self.title}', status={self.status})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert pitch deck to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "version": self.version,
            "template": self.template.value if self.template else None,
            "design_config": self.design_config,
            "branding": self.branding,
            "slide_order": self.slide_order,
            "total_slides": self.total_slides,
            "estimated_duration": self.estimated_duration,
            "generation_settings": self.generation_settings,
            "industry_focus": self.industry_focus,
            "target_audience": self.target_audience,
            "status": self.status.value if self.status else None,
            "is_public": self.is_public,
            "is_template": self.is_template,
            "view_count": self.view_count,
            "download_count": self.download_count,
            "share_count": self.share_count,
            "feedback_score": self.feedback_score,
            "feedback_comments": self.feedback_comments,
            "export_formats": self.export_formats,
            "last_exported": self.last_exported.isoformat() if self.last_exported else None,
            "export_settings": self.export_settings,
            "collaborators": self.collaborators,
            "permissions": self.permissions,
            "parent_version_id": str(self.parent_version_id) if self.parent_version_id else None,
            "version_history": self.version_history,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "startup_id": str(self.startup_id),
            "user_id": str(self.user_id),
            "slides": [slide.to_dict() for slide in self.slides] if self.slides else []
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PitchDeck":
        """Create pitch deck from dictionary"""
        # Convert enum values
        if "template" in data and data["template"]:
            data["template"] = PitchDeckTemplate(data["template"])
        if "status" in data and data["status"]:
            data["status"] = PitchDeckStatus(data["status"])
        
        return cls(**data)
    
    def add_slide(self, slide: "Slide") -> None:
        """Add a slide to the pitch deck"""
        slide.pitch_deck_id = self.id
        slide.order = len(self.slides) + 1
        self.slides.append(slide)
        self.total_slides = len(self.slides)
        self._update_slide_order()
    
    def remove_slide(self, slide_id: str) -> bool:
        """Remove a slide from the pitch deck"""
        slide = next((s for s in self.slides if str(s.id) == slide_id), None)
        if slide:
            self.slides.remove(slide)
            self.total_slides = len(self.slides)
            self._update_slide_order()
            return True
        return False
    
    def reorder_slides(self, new_order: List[str]) -> None:
        """Reorder slides in the pitch deck"""
        # Update slide order
        for i, slide_id in enumerate(new_order):
            slide = next((s for s in self.slides if str(s.id) == slide_id), None)
            if slide:
                slide.order = i + 1
        
        self._update_slide_order()
    
    def _update_slide_order(self) -> None:
        """Update the slide order array"""
        self.slide_order = [str(slide.id) for slide in sorted(self.slides, key=lambda x: x.order)]
    
    def get_slide_by_type(self, slide_type: str) -> Optional["Slide"]:
        """Get slide by type"""
        return next((slide for slide in self.slides if slide.slide_type == slide_type), None)
    
    def get_slides_by_type(self, slide_type: str) -> List["Slide"]:
        """Get all slides of a specific type"""
        return [slide for slide in self.slides if slide.slide_type == slide_type]
    
    def duplicate(self, new_title: str = None) -> "PitchDeck":
        """Create a duplicate of the pitch deck"""
        new_deck = PitchDeck(
            title=new_title or f"{self.title} (Copy)",
            description=self.description,
            template=self.template,
            design_config=self.design_config.copy() if self.design_config else None,
            branding=self.branding.copy() if self.branding else None,
            generation_settings=self.generation_settings.copy() if self.generation_settings else None,
            industry_focus=self.industry_focus,
            target_audience=self.target_audience,
            startup_id=self.startup_id,
            user_id=self.user_id,
            parent_version_id=self.id
        )
        
        # Copy slides
        for slide in self.slides:
            new_slide = slide.duplicate()
            new_deck.add_slide(new_slide)
        
        return new_deck 