from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from typing import Optional, List, Dict, Any

from ..database.connection import Base

class IndustryType(enum.Enum):
    """Industry types for startups"""
    SAAS = "saas"
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "ecommerce"
    AI_ML = "ai_ml"
    BIOTECH = "biotech"
    CONSUMER_GOODS = "consumer_goods"
    MARKETPLACE = "marketplace"
    MOBILE_APP = "mobile_app"
    HARDWARE = "hardware"
    CLEANTECH = "cleantech"
    EDUTECH = "edutech"
    REAL_ESTATE = "real_estate"
    OTHER = "other"

class FundingStage(enum.Enum):
    """Funding stages for startups"""
    IDEA = "idea"
    PRE_SEED = "pre_seed"
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    SERIES_D = "series_d"
    IPO = "ipo"
    ACQUIRED = "acquired"

class RevenueModel(enum.Enum):
    """Revenue models for startups"""
    SUBSCRIPTION = "subscription"
    MARKETPLACE = "marketplace"
    FREEMIUM = "freemium"
    ENTERPRISE = "enterprise"
    ADVERTISING = "advertising"
    TRANSACTION_FEE = "transaction_fee"
    LICENSING = "licensing"
    HARDWARE_SALES = "hardware_sales"
    CONSULTING = "consulting"
    OTHER = "other"

class Startup(Base):
    """Startup model for storing comprehensive startup information"""
    __tablename__ = "startups"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    name = Column(String(255), nullable=False, index=True)
    tagline = Column(String(500))
    description = Column(Text)
    website = Column(String(500))
    founded_date = Column(DateTime)
    
    # Industry and stage
    industry = Column(Enum(IndustryType), nullable=False, index=True)
    funding_stage = Column(Enum(FundingStage), nullable=False, index=True)
    revenue_model = Column(Enum(RevenueModel), nullable=False)
    
    # Problem and solution
    problem_statement = Column(Text)
    solution_description = Column(Text)
    unique_value_proposition = Column(Text)
    
    # Market information
    target_market = Column(Text)
    market_size_tam = Column(Float)  # Total Addressable Market
    market_size_sam = Column(Float)  # Serviceable Addressable Market
    market_size_som = Column(Float)  # Serviceable Obtainable Market
    market_growth_rate = Column(Float)
    
    # Business metrics
    current_revenue = Column(Float)
    monthly_recurring_revenue = Column(Float)
    annual_recurring_revenue = Column(Float)
    customer_count = Column(Integer)
    user_count = Column(Integer)
    growth_rate = Column(Float)
    
    # Financial information
    burn_rate = Column(Float)
    runway_months = Column(Float)
    unit_economics = Column(JSON)  # CAC, LTV, etc.
    financial_projections = Column(JSON)  # 3-5 year projections
    
    # Competition
    competitors = Column(JSON)  # List of competitor information
    competitive_advantages = Column(Text)
    
    # Team information
    team_size = Column(Integer)
    team_experience = Column(Text)
    key_team_members = Column(JSON)  # List of team member details
    
    # Funding information
    total_funding_raised = Column(Float)
    funding_rounds = Column(JSON)  # List of funding rounds
    current_valuation = Column(Float)
    funding_ask = Column(Float)
    use_of_funds = Column(Text)
    
    # Traction and milestones
    key_metrics = Column(JSON)  # KPIs and metrics
    achievements = Column(Text)
    milestones = Column(JSON)  # Past and future milestones
    
    # Technology and product
    technology_stack = Column(JSON)
    product_features = Column(JSON)
    roadmap = Column(JSON)
    
    # Marketing and sales
    marketing_strategy = Column(Text)
    sales_process = Column(Text)
    customer_acquisition_channels = Column(JSON)
    
    # Risk factors
    risk_factors = Column(JSON)
    mitigation_strategies = Column(Text)
    
    # Additional information
    regulatory_environment = Column(Text)
    intellectual_property = Column(Text)
    partnerships = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # User relationship
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="startups")
    
    # Pitch deck relationship
    pitch_decks = relationship("PitchDeck", back_populates="startup", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Startup(id={self.id}, name='{self.name}', industry={self.industry})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert startup to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "tagline": self.tagline,
            "description": self.description,
            "website": self.website,
            "founded_date": self.founded_date.isoformat() if self.founded_date else None,
            "industry": self.industry.value if self.industry else None,
            "funding_stage": self.funding_stage.value if self.funding_stage else None,
            "revenue_model": self.revenue_model.value if self.revenue_model else None,
            "problem_statement": self.problem_statement,
            "solution_description": self.solution_description,
            "unique_value_proposition": self.unique_value_proposition,
            "target_market": self.target_market,
            "market_size_tam": self.market_size_tam,
            "market_size_sam": self.market_size_sam,
            "market_size_som": self.market_size_som,
            "market_growth_rate": self.market_growth_rate,
            "current_revenue": self.current_revenue,
            "monthly_recurring_revenue": self.monthly_recurring_revenue,
            "annual_recurring_revenue": self.annual_recurring_revenue,
            "customer_count": self.customer_count,
            "user_count": self.user_count,
            "growth_rate": self.growth_rate,
            "burn_rate": self.burn_rate,
            "runway_months": self.runway_months,
            "unit_economics": self.unit_economics,
            "financial_projections": self.financial_projections,
            "competitors": self.competitors,
            "competitive_advantages": self.competitive_advantages,
            "team_size": self.team_size,
            "team_experience": self.team_experience,
            "key_team_members": self.key_team_members,
            "total_funding_raised": self.total_funding_raised,
            "funding_rounds": self.funding_rounds,
            "current_valuation": self.current_valuation,
            "funding_ask": self.funding_ask,
            "use_of_funds": self.use_of_funds,
            "key_metrics": self.key_metrics,
            "achievements": self.achievements,
            "milestones": self.milestones,
            "technology_stack": self.technology_stack,
            "product_features": self.product_features,
            "roadmap": self.roadmap,
            "marketing_strategy": self.marketing_strategy,
            "sales_process": self.sales_process,
            "customer_acquisition_channels": self.customer_acquisition_channels,
            "risk_factors": self.risk_factors,
            "mitigation_strategies": self.mitigation_strategies,
            "regulatory_environment": self.regulatory_environment,
            "intellectual_property": self.intellectual_property,
            "partnerships": self.partnerships,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "user_id": str(self.user_id)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Startup":
        """Create startup from dictionary"""
        # Convert enum values
        if "industry" in data and data["industry"]:
            data["industry"] = IndustryType(data["industry"])
        if "funding_stage" in data and data["funding_stage"]:
            data["funding_stage"] = FundingStage(data["funding_stage"])
        if "revenue_model" in data and data["revenue_model"]:
            data["revenue_model"] = RevenueModel(data["revenue_model"])
        
        return cls(**data) 