"""
Rate limiting utilities
"""
import os
import time
import structlog
from typing import Dict, Optional
from fastapi import HTTPException, status
from datetime import datetime, timedelta

logger = structlog.get_logger()

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests: Dict[str, list] = {}
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
        self.rate_limit_per_hour = int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if a request is allowed"""
        current_time = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 3600  # Keep last hour
        ]
        
        # Check rate limits
        requests_last_minute = len([
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 60
        ])
        
        requests_last_hour = len(self.requests[client_id])
        
        if requests_last_minute >= self.rate_limit_per_minute:
            logger.warning("Rate limit exceeded per minute", client_id=client_id)
            return False
        
        if requests_last_hour >= self.rate_limit_per_hour:
            logger.warning("Rate limit exceeded per hour", client_id=client_id)
            return False
        
        # Add current request
        self.requests[client_id].append(current_time)
        return True
    
    def get_remaining_requests(self, client_id: str) -> Dict[str, int]:
        """Get remaining requests for a client"""
        current_time = time.time()
        
        if client_id not in self.requests:
            return {
                "per_minute": self.rate_limit_per_minute,
                "per_hour": self.rate_limit_per_hour
            }
        
        requests_last_minute = len([
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 60
        ])
        
        requests_last_hour = len([
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 3600
        ])
        
        return {
            "per_minute": max(0, self.rate_limit_per_minute - requests_last_minute),
            "per_hour": max(0, self.rate_limit_per_hour - requests_last_hour)
        }

# Global rate limiter instance
rate_limiter = RateLimiter()

def check_rate_limit(client_id: str):
    """Check rate limit for a client"""
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        ) 