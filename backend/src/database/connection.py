from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
import structlog
from typing import Optional
from contextlib import contextmanager

logger = structlog.get_logger()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/pitchdeck")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

# Create engine
if os.getenv("TESTING"):
    # Use SQLite for testing
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
else:
    # Use PostgreSQL for production
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=os.getenv("DEBUG", "false").lower() == "true"
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

# Global session variable
_db: Optional[Session] = None

def get_db() -> Session:
    """Get database session"""
    global _db
    if _db is None:
        _db = SessionLocal()
    return _db

def close_db() -> None:
    """Close database session"""
    global _db
    if _db is not None:
        _db.close()
        _db = None

async def init_db() -> None:
    """Initialize database tables"""
    try:
        # Import all models to ensure they are registered
        from ..models import user, startup, pitch_deck, slide
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Create initial data if needed
        await create_initial_data()
        
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise

async def create_initial_data() -> None:
    """Create initial data for the application"""
    try:
        db = get_db()
        
        # Check if admin user exists
        from ..models.user import User, UserRole, SubscriptionPlan, UserStatus
        
        admin_user = db.query(User).filter(User.email == "admin@ai-pitch-deck.com").first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                email="admin@ai-pitch-deck.com",
                first_name="Admin",
                last_name="User",
                role=UserRole.SUPER_ADMIN,
                subscription_plan=SubscriptionPlan.ENTERPRISE,
                subscription_status=UserStatus.ACTIVE,
                is_email_verified=True
            )
            admin_user.set_password("admin123")  # Change in production
            db.add(admin_user)
            db.commit()
            logger.info("Admin user created successfully")
        
        # Create default templates and configurations
        await create_default_templates(db)
        
    except Exception as e:
        logger.error("Failed to create initial data", error=str(e))
        db.rollback()
        raise
    finally:
        close_db()

async def create_default_templates(db: Session) -> None:
    """Create default pitch deck templates"""
    try:
        from ..models.pitch_deck import PitchDeck, PitchDeckTemplate, PitchDeckStatus
        
        # Check if default templates exist
        existing_templates = db.query(PitchDeck).filter(PitchDeck.is_template == True).count()
        
        if existing_templates == 0:
            # Create default templates
            default_templates = [
                {
                    "title": "Classic Startup Pitch Deck",
                    "description": "Traditional pitch deck format with proven structure",
                    "template": PitchDeckTemplate.CLASSIC,
                    "design_config": {
                        "color_scheme": "professional",
                        "font_family": "Arial",
                        "layout_style": "clean"
                    }
                },
                {
                    "title": "Modern Startup Pitch Deck",
                    "description": "Contemporary design with modern visual elements",
                    "template": PitchDeckTemplate.MODERN,
                    "design_config": {
                        "color_scheme": "modern",
                        "font_family": "Helvetica",
                        "layout_style": "minimal"
                    }
                },
                {
                    "title": "Minimalist Pitch Deck",
                    "description": "Clean and simple design focusing on content",
                    "template": PitchDeckTemplate.MINIMAL,
                    "design_config": {
                        "color_scheme": "minimal",
                        "font_family": "Inter",
                        "layout_style": "sparse"
                    }
                }
            ]
            
            for template_data in default_templates:
                template = PitchDeck(
                    title=template_data["title"],
                    description=template_data["description"],
                    template=template_data["template"],
                    design_config=template_data["design_config"],
                    is_template=True,
                    status=PitchDeckStatus.PUBLISHED,
                    user_id=db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first().id
                )
                db.add(template)
            
            db.commit()
            logger.info("Default templates created successfully")
            
    except Exception as e:
        logger.error("Failed to create default templates", error=str(e))
        db.rollback()
        raise

@contextmanager
def get_db_context():
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def health_check() -> bool:
    """Check database health"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return False

# Database utilities
def execute_raw_sql(sql: str, params: dict = None) -> list:
    """Execute raw SQL query"""
    db = get_db()
    try:
        result = db.execute(sql, params or {})
        return result.fetchall()
    finally:
        close_db()

def get_table_count(table_name: str) -> int:
    """Get row count for a table"""
    db = get_db()
    try:
        result = db.execute(f"SELECT COUNT(*) FROM {table_name}")
        return result.scalar()
    finally:
        close_db()

# Migration utilities
def create_migration(message: str) -> None:
    """Create a new migration"""
    import subprocess
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    migration_name = f"{timestamp}_{message.lower().replace(' ', '_')}"
    
    try:
        subprocess.run([
            "alembic", "revision", 
            "--autogenerate", 
            "-m", message,
            "--rev-id", migration_name
        ], check=True)
        logger.info(f"Migration created: {migration_name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create migration: {e}")
        raise

def run_migrations() -> None:
    """Run database migrations"""
    import subprocess
    
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logger.info("Database migrations completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run migrations: {e}")
        raise 