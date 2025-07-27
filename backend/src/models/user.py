from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from typing import Optional, List, Dict, Any
from passlib.hash import bcrypt

from ..database.connection import Base

class UserRole(enum.Enum):
    """User roles in the system"""
    FREE_USER = "free_user"
    PREMIUM_USER = "premium_user"
    ENTERPRISE_USER = "enterprise_user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class SubscriptionPlan(enum.Enum):
    """Subscription plan types"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

class UserStatus(enum.Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class User(Base):
    """User model for authentication and user management"""
    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255))
    email_verification_expires = Column(DateTime)
    
    # Profile information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    company_name = Column(String(255))
    job_title = Column(String(255))
    phone_number = Column(String(50))
    website = Column(String(500))
    
    # Profile picture and branding
    profile_picture_url = Column(String(500))
    company_logo_url = Column(String(500))
    brand_colors = Column(JSON)  # Primary and secondary brand colors
    
    # Location and timezone
    country = Column(String(100))
    city = Column(String(100))
    timezone = Column(String(50), default="UTC")
    
    # Role and subscription
    role = Column(Enum(UserRole), default=UserRole.FREE_USER)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    subscription_status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    
    # Subscription details
    subscription_start_date = Column(DateTime)
    subscription_end_date = Column(DateTime)
    subscription_id = Column(String(255))  # External subscription ID
    billing_email = Column(String(255))
    
    # Usage tracking
    pitch_decks_created = Column(Integer, default=0)
    total_generations = Column(Integer, default=0)
    api_calls_used = Column(Integer, default=0)
    api_calls_limit = Column(Integer, default=10)  # Free tier limit
    
    # Preferences and settings
    preferences = Column(JSON)  # User preferences and settings
    notification_settings = Column(JSON)  # Email notification preferences
    ai_model_preferences = Column(JSON)  # Preferred AI models
    
    # Social and professional
    linkedin_url = Column(String(500))
    twitter_url = Column(String(500))
    github_url = Column(String(500))
    bio = Column(Text)
    
    # Security
    last_login = Column(DateTime)
    last_password_change = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255))
    
    # Analytics and tracking
    signup_source = Column(String(100))  # How user found the platform
    referrer_code = Column(String(100))
    referred_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime)  # Soft delete
    
    # Relationships
    startups = relationship("Startup", back_populates="user", cascade="all, delete-orphan")
    pitch_decks = relationship("PitchDeck", back_populates="user", cascade="all, delete-orphan")
    referred_users = relationship("User", backref=ForeignKey("users.id"))
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role={self.role})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self) -> bool:
        """Check if user account is active"""
        return self.subscription_status == UserStatus.ACTIVE and not self.deleted_at
    
    @property
    def is_premium(self) -> bool:
        """Check if user has premium subscription"""
        return self.subscription_plan in [SubscriptionPlan.BASIC, SubscriptionPlan.PRO, SubscriptionPlan.ENTERPRISE]
    
    @property
    def is_enterprise(self) -> bool:
        """Check if user has enterprise subscription"""
        return self.subscription_plan == SubscriptionPlan.ENTERPRISE
    
    @property
    def api_calls_remaining(self) -> int:
        """Get remaining API calls"""
        return max(0, self.api_calls_limit - self.api_calls_used)
    
    def set_password(self, password: str) -> None:
        """Set user password with bcrypt hashing"""
        self.password_hash = bcrypt.hash(password)
        self.last_password_change = func.now()
    
    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        return bcrypt.verify(password, self.password_hash)
    
    def increment_api_calls(self, count: int = 1) -> None:
        """Increment API call usage"""
        self.api_calls_used += count
        self.updated_at = func.now()
    
    def increment_generations(self, count: int = 1) -> None:
        """Increment generation count"""
        self.total_generations += count
        self.updated_at = func.now()
    
    def increment_pitch_decks(self, count: int = 1) -> None:
        """Increment pitch deck creation count"""
        self.pitch_decks_created += count
        self.updated_at = func.now()
    
    def can_create_pitch_deck(self) -> bool:
        """Check if user can create a new pitch deck"""
        if self.is_enterprise:
            return True
        
        # Free users limited to 3 pitch decks
        if self.subscription_plan == SubscriptionPlan.FREE:
            return self.pitch_decks_created < 3
        
        return True
    
    def can_use_ai_generation(self) -> bool:
        """Check if user can use AI generation"""
        if self.is_enterprise:
            return True
        
        # Free users limited to 10 generations
        if self.subscription_plan == SubscriptionPlan.FREE:
            return self.total_generations < 10
        
        return True
    
    def can_make_api_call(self) -> bool:
        """Check if user can make an API call"""
        return self.api_calls_remaining > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary (excluding sensitive data)"""
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "company_name": self.company_name,
            "job_title": self.job_title,
            "phone_number": self.phone_number,
            "website": self.website,
            "profile_picture_url": self.profile_picture_url,
            "company_logo_url": self.company_logo_url,
            "brand_colors": self.brand_colors,
            "country": self.country,
            "city": self.city,
            "timezone": self.timezone,
            "role": self.role.value if self.role else None,
            "subscription_plan": self.subscription_plan.value if self.subscription_plan else None,
            "subscription_status": self.subscription_status.value if self.subscription_status else None,
            "subscription_start_date": self.subscription_start_date.isoformat() if self.subscription_start_date else None,
            "subscription_end_date": self.subscription_end_date.isoformat() if self.subscription_end_date else None,
            "pitch_decks_created": self.pitch_decks_created,
            "total_generations": self.total_generations,
            "api_calls_used": self.api_calls_used,
            "api_calls_limit": self.api_calls_limit,
            "api_calls_remaining": self.api_calls_remaining,
            "preferences": self.preferences,
            "notification_settings": self.notification_settings,
            "ai_model_preferences": self.ai_model_preferences,
            "linkedin_url": self.linkedin_url,
            "twitter_url": self.twitter_url,
            "github_url": self.github_url,
            "bio": self.bio,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "two_factor_enabled": self.two_factor_enabled,
            "signup_source": self.signup_source,
            "referrer_code": self.referrer_code,
            "referred_by": str(self.referred_by) if self.referred_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "is_premium": self.is_premium,
            "is_enterprise": self.is_enterprise
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create user from dictionary"""
        # Convert enum values
        if "role" in data and data["role"]:
            data["role"] = UserRole(data["role"])
        if "subscription_plan" in data and data["subscription_plan"]:
            data["subscription_plan"] = SubscriptionPlan(data["subscription_plan"])
        if "subscription_status" in data and data["subscription_status"]:
            data["subscription_status"] = UserStatus(data["subscription_status"])
        
        return cls(**data)
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.last_login = func.now()
    
    def lock_account(self, duration_minutes: int = 30) -> None:
        """Lock user account for specified duration"""
        from datetime import datetime, timedelta
        self.account_locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.failed_login_attempts += 1
    
    def unlock_account(self) -> None:
        """Unlock user account"""
        self.account_locked_until = None
        self.failed_login_attempts = 0
    
    def is_account_locked(self) -> bool:
        """Check if account is currently locked"""
        if not self.account_locked_until:
            return False
        return self.account_locked_until > func.now()
    
    def get_subscription_expiry_days(self) -> Optional[int]:
        """Get days until subscription expires"""
        if not self.subscription_end_date:
            return None
        
        from datetime import datetime
        delta = self.subscription_end_date - datetime.utcnow()
        return max(0, delta.days) 