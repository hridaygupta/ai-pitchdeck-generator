import openai
import anthropic
import os
import json
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from ..models.startup import Startup, IndustryType
from ..models.slide import Slide, SlideType
from ..utils.prompt_templates import get_prompt_template

logger = structlog.get_logger()

# Configure AI clients
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    try:
        openai_client = openai.OpenAI(api_key=openai_api_key)
    except Exception as e:
        logger.warning(f"Failed to initialize OpenAI client: {e}")
        openai_client = None
else:
    openai_client = None

# Initialize Anthropic client with proper configuration
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if anthropic_api_key:
    try:
        anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
    except Exception as e:
        logger.warning(f"Failed to initialize Anthropic client: {e}")
        anthropic_client = None
else:
    anthropic_client = None

class ContentGenerator:
    """AI-powered content generator for pitch deck slides"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.model_preferences = {
            "content": "gpt-4",  # OpenAI GPT-4 for content generation
            "analysis": "claude-3-sonnet-20240229",  # Claude for analysis
            "creative": "gpt-4",  # GPT-4 for creative content
            "technical": "claude-3-sonnet-20240229"  # Claude for technical content
        }
    
    async def generate_pitch_deck_content(self, startup: Startup, slide_types: List[SlideType] = None) -> List[Dict[str, Any]]:
        """Generate content for all slides in a pitch deck"""
        try:
            logger.info("Starting pitch deck content generation", startup_id=str(startup.id))
            
            # Default slide types if not specified
            if not slide_types:
                slide_types = [
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
            
            # Generate content for each slide type
            slides_content = []
            tasks = []
            
            for slide_type in slide_types:
                task = self.generate_slide_content(startup, slide_type)
                tasks.append(task)
            
            # Execute all generation tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to generate content for {slide_types[i]}", error=str(result))
                    # Create fallback content
                    slides_content.append(self._create_fallback_content(slide_types[i], startup))
                else:
                    slides_content.append(result)
            
            logger.info("Pitch deck content generation completed", 
                       startup_id=str(startup.id), 
                       slides_count=len(slides_content))
            
            return slides_content
            
        except Exception as e:
            logger.error("Failed to generate pitch deck content", error=str(e))
            raise
    
    async def generate_slide_content(self, startup: Startup, slide_type: SlideType) -> Dict[str, Any]:
        """Generate content for a specific slide type"""
        try:
            logger.info(f"Generating content for {slide_type.value} slide", startup_id=str(startup.id))
            
            # Get industry-specific prompt template
            prompt_template = get_prompt_template(slide_type, startup.industry)
            
            # Prepare context data
            context_data = self._prepare_context_data(startup, slide_type)
            
            # Generate content based on slide type
            if slide_type == SlideType.TITLE:
                content = await self._generate_title_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.PROBLEM:
                content = await self._generate_problem_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.SOLUTION:
                content = await self._generate_solution_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.MARKET_OPPORTUNITY:
                content = await self._generate_market_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.BUSINESS_MODEL:
                content = await self._generate_business_model_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.TRACTION:
                content = await self._generate_traction_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.COMPETITION:
                content = await self._generate_competition_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.TEAM:
                content = await self._generate_team_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.FINANCIALS:
                content = await self._generate_financials_slide(startup, prompt_template, context_data)
            elif slide_type == SlideType.FUNDING_ASK:
                content = await self._generate_funding_slide(startup, prompt_template, context_data)
            else:
                content = await self._generate_custom_slide(startup, slide_type, prompt_template, context_data)
            
            return {
                "slide_type": slide_type.value,
                "content": content,
                "generated_at": datetime.utcnow().isoformat(),
                "model_used": self.model_preferences["content"]
            }
            
        except Exception as e:
            logger.error(f"Failed to generate {slide_type.value} slide content", error=str(e))
            raise
    
    async def _generate_title_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate title slide content"""
        prompt = prompt_template.format(
            company_name=startup.name,
            tagline=startup.tagline or "",
            industry=startup.industry.value,
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=200)
        
        return {
            "title": startup.name,
            "subtitle": startup.tagline,
            "content": {
                "headline": response.get("headline", startup.name),
                "subheadline": response.get("subheadline", startup.tagline),
                "presenter_info": response.get("presenter_info", ""),
                "date": datetime.now().strftime("%B %Y")
            },
            "layout": "title_center"
        }
    
    async def _generate_problem_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate problem slide content"""
        prompt = prompt_template.format(
            problem_statement=startup.problem_statement or "",
            industry=startup.industry.value,
            target_market=startup.target_market or "",
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": "The Problem",
            "content": {
                "problem_statement": response.get("problem_statement", startup.problem_statement),
                "pain_points": response.get("pain_points", []),
                "market_size_impact": response.get("market_size_impact", ""),
                "urgency": response.get("urgency", "")
            },
            "bullet_points": response.get("pain_points", []),
            "layout": "bullet_points"
        }
    
    async def _generate_solution_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate solution slide content"""
        prompt = prompt_template.format(
            solution_description=startup.solution_description or "",
            unique_value_proposition=startup.unique_value_proposition or "",
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": "Our Solution",
            "content": {
                "solution_overview": response.get("solution_overview", startup.solution_description),
                "key_features": response.get("key_features", []),
                "unique_advantages": response.get("unique_advantages", []),
                "value_proposition": response.get("value_proposition", startup.unique_value_proposition)
            },
            "bullet_points": response.get("key_features", []),
            "layout": "two_column"
        }
    
    async def _generate_market_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market opportunity slide content"""
        prompt = prompt_template.format(
            market_size_tam=startup.market_size_tam or 0,
            market_size_sam=startup.market_size_sam or 0,
            market_size_som=startup.market_size_som or 0,
            market_growth_rate=startup.market_growth_rate or 0,
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=500)
        
        return {
            "title": "Market Opportunity",
            "content": {
                "market_overview": response.get("market_overview", ""),
                "market_size": {
                    "tam": startup.market_size_tam,
                    "sam": startup.market_size_sam,
                    "som": startup.market_size_som
                },
                "growth_drivers": response.get("growth_drivers", []),
                "market_timing": response.get("market_timing", "")
            },
            "key_metrics": [
                {"name": "TAM", "value": startup.market_size_tam, "unit": "USD"},
                {"name": "SAM", "value": startup.market_size_sam, "unit": "USD"},
                {"name": "SOM", "value": startup.market_size_som, "unit": "USD"},
                {"name": "Growth Rate", "value": startup.market_growth_rate, "unit": "%"}
            ],
            "layout": "chart"
        }
    
    async def _generate_business_model_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate business model slide content"""
        prompt = prompt_template.format(
            revenue_model=startup.revenue_model.value,
            current_revenue=startup.current_revenue or 0,
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": "Business Model",
            "content": {
                "revenue_streams": response.get("revenue_streams", []),
                "pricing_strategy": response.get("pricing_strategy", ""),
                "customer_segments": response.get("customer_segments", []),
                "cost_structure": response.get("cost_structure", "")
            },
            "bullet_points": response.get("revenue_streams", []),
            "layout": "grid"
        }
    
    async def _generate_traction_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate traction slide content"""
        prompt = prompt_template.format(
            customer_count=startup.customer_count or 0,
            user_count=startup.user_count or 0,
            growth_rate=startup.growth_rate or 0,
            achievements=startup.achievements or "",
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": "Traction & Milestones",
            "content": {
                "key_metrics": response.get("key_metrics", []),
                "achievements": response.get("achievements", []),
                "growth_trajectory": response.get("growth_trajectory", ""),
                "customer_testimonials": response.get("customer_testimonials", [])
            },
            "key_metrics": [
                {"name": "Customers", "value": startup.customer_count, "unit": ""},
                {"name": "Users", "value": startup.user_count, "unit": ""},
                {"name": "Growth Rate", "value": startup.growth_rate, "unit": "%"},
                {"name": "Revenue", "value": startup.current_revenue, "unit": "USD"}
            ],
            "layout": "grid"
        }
    
    async def _generate_competition_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competition slide content"""
        competitors = startup.competitors or []
        competitive_advantages = startup.competitive_advantages or ""
        
        prompt = prompt_template.format(
            competitors=json.dumps(competitors),
            competitive_advantages=competitive_advantages,
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": "Competitive Landscape",
            "content": {
                "competitor_analysis": response.get("competitor_analysis", []),
                "competitive_advantages": response.get("competitive_advantages", []),
                "market_positioning": response.get("market_positioning", ""),
                "differentiation": response.get("differentiation", "")
            },
            "bullet_points": response.get("competitive_advantages", []),
            "layout": "comparison"
        }
    
    async def _generate_team_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate team slide content"""
        team_members = startup.key_team_members or []
        team_experience = startup.team_experience or ""
        
        prompt = prompt_template.format(
            team_size=startup.team_size or 0,
            team_experience=team_experience,
            team_members=json.dumps(team_members),
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": "Our Team",
            "content": {
                "team_overview": response.get("team_overview", ""),
                "key_members": response.get("key_members", []),
                "expertise_areas": response.get("expertise_areas", []),
                "advisors": response.get("advisors", [])
            },
            "bullet_points": response.get("expertise_areas", []),
            "layout": "grid"
        }
    
    async def _generate_financials_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financials slide content"""
        financial_projections = startup.financial_projections or {}
        unit_economics = startup.unit_economics or {}
        
        prompt = prompt_template.format(
            current_revenue=startup.current_revenue or 0,
            burn_rate=startup.burn_rate or 0,
            runway_months=startup.runway_months or 0,
            financial_projections=json.dumps(financial_projections),
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=500)
        
        return {
            "title": "Financial Projections",
            "content": {
                "revenue_projections": response.get("revenue_projections", {}),
                "unit_economics": response.get("unit_economics", {}),
                "funding_utilization": response.get("funding_utilization", ""),
                "path_to_profitability": response.get("path_to_profitability", "")
            },
            "key_metrics": [
                {"name": "Current Revenue", "value": startup.current_revenue, "unit": "USD"},
                {"name": "Burn Rate", "value": startup.burn_rate, "unit": "USD/month"},
                {"name": "Runway", "value": startup.runway_months, "unit": "months"}
            ],
            "layout": "chart"
        }
    
    async def _generate_funding_slide(self, startup: Startup, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate funding ask slide content"""
        prompt = prompt_template.format(
            funding_ask=startup.funding_ask or 0,
            use_of_funds=startup.use_of_funds or "",
            current_valuation=startup.current_valuation or 0,
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": "Funding Ask",
            "content": {
                "funding_amount": response.get("funding_amount", startup.funding_ask),
                "use_of_funds": response.get("use_of_funds", []),
                "valuation": response.get("valuation", startup.current_valuation),
                "milestones": response.get("milestones", [])
            },
            "bullet_points": response.get("use_of_funds", []),
            "layout": "bullet_points"
        }
    
    async def _generate_custom_slide(self, startup: Startup, slide_type: SlideType, prompt_template: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate custom slide content"""
        prompt = prompt_template.format(
            slide_type=slide_type.value,
            **context_data
        )
        
        response = await self._call_openai(prompt, max_tokens=400)
        
        return {
            "title": response.get("title", slide_type.value.title()),
            "content": response.get("content", {}),
            "bullet_points": response.get("bullet_points", []),
            "layout": response.get("layout", "bullet_points")
        }
    
    async def _call_openai(self, prompt: str, max_tokens: int = 400) -> Dict[str, Any]:
        """Call OpenAI API for content generation"""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor,
                lambda: openai_client.chat.completions.create(
                    model=self.model_preferences["content"],
                    messages=[
                        {"role": "system", "content": "You are an expert pitch deck content generator. Generate professional, compelling content for startup pitch decks."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
            )
            
            content = response.choices[0].message.content
            return json.loads(content) if content.startswith('{') else {"content": content}
            
        except Exception as e:
            logger.error("OpenAI API call failed", error=str(e))
            raise
    
    def _prepare_context_data(self, startup: Startup, slide_type: SlideType) -> Dict[str, Any]:
        """Prepare context data for content generation"""
        return {
            "company_name": startup.name,
            "industry": startup.industry.value,
            "funding_stage": startup.funding_stage.value,
            "revenue_model": startup.revenue_model.value,
            "target_market": startup.target_market or "",
            "problem_statement": startup.problem_statement or "",
            "solution_description": startup.solution_description or "",
            "unique_value_proposition": startup.unique_value_proposition or "",
            "team_size": startup.team_size or 0,
            "customer_count": startup.customer_count or 0,
            "current_revenue": startup.current_revenue or 0,
            "funding_ask": startup.funding_ask or 0,
            "slide_type": slide_type.value
        }
    
    def _create_fallback_content(self, slide_type: SlideType, startup: Startup) -> Dict[str, Any]:
        """Create fallback content when AI generation fails"""
        fallback_content = {
            "slide_type": slide_type.value,
            "content": {
                "title": slide_type.value.replace("_", " ").title(),
                "content": f"Content for {slide_type.value} slide",
                "bullet_points": ["Sample bullet point 1", "Sample bullet point 2"],
                "layout": "bullet_points"
            },
            "generated_at": datetime.utcnow().isoformat(),
            "model_used": "fallback"
        }
        
        return fallback_content 