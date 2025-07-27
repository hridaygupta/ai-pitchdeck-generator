"""
Celery configuration for background tasks
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('ENVIRONMENT', 'development')

# Create celery app
celery_app = Celery(
    'ai_pitch_deck',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0'),
    include=[
        'src.tasks.generation_tasks',
        'src.tasks.export_tasks',
        'src.tasks.market_research_tasks',
        'src.tasks.financial_modeling_tasks',
        'src.tasks.analytics_tasks',
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    broker_connection_retry_on_startup=True,
)

# Periodic tasks
celery_app.conf.beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'src.tasks.analytics_tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'generate-analytics-report': {
        'task': 'src.tasks.analytics_tasks.generate_daily_analytics',
        'schedule': crontab(hour=6, minute=0),  # Daily at 6 AM
    },
    'update-market-data': {
        'task': 'src.tasks.market_research_tasks.update_market_data',
        'schedule': crontab(minute=0, hour='*/4'),  # Every 4 hours
    },
    'backup-database': {
        'task': 'src.tasks.analytics_tasks.backup_database',
        'schedule': crontab(hour=1, minute=0),  # Daily at 1 AM
    },
}

if __name__ == '__main__':
    celery_app.start() 