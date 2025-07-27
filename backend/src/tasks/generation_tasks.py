"""
Background tasks for pitch deck generation
"""
import os
import structlog
from celery import shared_task
from typing import Dict, Any
import asyncio

from ..ai.content_generator import ContentGenerator
from ..ai.market_researcher import MarketResearcher
from ..ai.financial_modeler import FinancialModeler

logger = structlog.get_logger()

@shared_task
def generate_pitch_deck_background(startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """Background task to generate a complete pitch deck"""
    try:
        logger.info("Starting background pitch deck generation", startup_name=startup_data.get("name"))
        
        # Create AI service instances
        content_generator = ContentGenerator()
        market_researcher = MarketResearcher()
        financial_modeler = FinancialModeler()
        
        # Run async tasks in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Generate content
            slides_content = loop.run_until_complete(
                content_generator.generate_pitch_deck_content(startup_data)
            )
            
            # Get market research
            market_data = loop.run_until_complete(
                market_researcher.get_market_data(startup_data.get("industry", "technology"))
            )
            
            # Create financial model
            financial_model = loop.run_until_complete(
                financial_modeler.create_financial_model(startup_data)
            )
            
            result = {
                "status": "completed",
                "slides_content": slides_content,
                "market_data": market_data,
                "financial_model": financial_model,
                "startup_name": startup_data.get("name")
            }
            
            logger.info("Background pitch deck generation completed", startup_name=startup_data.get("name"))
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Background pitch deck generation failed", error=str(e))
        return {
            "status": "failed",
            "error": str(e),
            "startup_name": startup_data.get("name")
        }

@shared_task
def generate_single_slide_background(startup_data: Dict[str, Any], slide_type: str) -> Dict[str, Any]:
    """Background task to generate a single slide"""
    try:
        logger.info("Starting single slide generation", slide_type=slide_type)
        
        content_generator = ContentGenerator()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            from ..models.slide import SlideType
            slide_type_enum = SlideType(slide_type)
            
            content = loop.run_until_complete(
                content_generator.generate_slide_content(startup_data, slide_type_enum)
            )
            
            result = {
                "status": "completed",
                "slide_content": content,
                "slide_type": slide_type
            }
            
            logger.info("Single slide generation completed", slide_type=slide_type)
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Single slide generation failed", error=str(e))
        return {
            "status": "failed",
            "error": str(e),
            "slide_type": slide_type
        }

@shared_task
def generate_market_research_background(startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """Background task to generate market research"""
    try:
        logger.info("Starting market research generation")
        
        market_researcher = MarketResearcher()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            market_data = loop.run_until_complete(
                market_researcher.get_market_data(startup_data.get("industry", "technology"))
            )
            
            competitor_analysis = loop.run_until_complete(
                market_researcher.get_competitor_analysis(
                    startup_data.get("name", ""),
                    startup_data.get("industry", "technology")
                )
            )
            
            tam_sam_som = loop.run_until_complete(
                market_researcher.calculate_tam_sam_som(
                    startup_data.get("industry", "technology"),
                    startup_data.get("target_market", "")
                )
            )
            
            result = {
                "status": "completed",
                "market_data": market_data,
                "competitor_analysis": competitor_analysis,
                "tam_sam_som": tam_sam_som
            }
            
            logger.info("Market research generation completed")
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Market research generation failed", error=str(e))
        return {
            "status": "failed",
            "error": str(e)
        }

@shared_task
def generate_financial_model_background(startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """Background task to generate financial model"""
    try:
        logger.info("Starting financial model generation")
        
        financial_modeler = FinancialModeler()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            financial_model = loop.run_until_complete(
                financial_modeler.create_financial_model(startup_data)
            )
            
            result = {
                "status": "completed",
                "financial_model": financial_model
            }
            
            logger.info("Financial model generation completed")
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Financial model generation failed", error=str(e))
        return {
            "status": "failed",
            "error": str(e)
        } 