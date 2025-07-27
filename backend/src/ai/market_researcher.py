"""
Market research module for collecting and analyzing market data
"""
import os
import asyncio
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
import pandas as pd

logger = structlog.get_logger()

class MarketResearcher:
    """Market research and data collection for startups"""
    
    def __init__(self):
        self.crunchbase_api_key = os.getenv("CRUNCHBASE_API_KEY")
        self.pitchbook_api_key = os.getenv("PITCHBOOK_API_KEY")
        
    async def get_market_data(self, industry: str, market_size: str = None) -> Dict[str, Any]:
        """Get comprehensive market data for an industry"""
        try:
            logger.info("Starting market research", industry=industry)
            
            # Collect data from multiple sources
            market_data = {
                "industry": industry,
                "timestamp": datetime.utcnow().isoformat(),
                "market_size": await self._get_market_size(industry),
                "growth_rate": await self._get_growth_rate(industry),
                "key_players": await self._get_key_players(industry),
                "trends": await self._get_market_trends(industry),
                "regulations": await self._get_regulations(industry),
                "risks": await self._get_market_risks(industry)
            }
            
            logger.info("Market research completed", industry=industry)
            return market_data
            
        except Exception as e:
            logger.error("Market research failed", industry=industry, error=str(e))
            return self._create_fallback_market_data(industry)
    
    async def get_competitor_analysis(self, startup_name: str, industry: str) -> Dict[str, Any]:
        """Analyze competitors in the market"""
        try:
            logger.info("Starting competitor analysis", startup=startup_name, industry=industry)
            
            competitors = await self._find_competitors(startup_name, industry)
            
            analysis = {
                "startup_name": startup_name,
                "industry": industry,
                "timestamp": datetime.utcnow().isoformat(),
                "competitors": competitors,
                "competitive_landscape": await self._analyze_competitive_landscape(competitors),
                "differentiation_opportunities": await self._find_differentiation_opportunities(competitors)
            }
            
            logger.info("Competitor analysis completed", startup=startup_name)
            return analysis
            
        except Exception as e:
            logger.error("Competitor analysis failed", startup=startup_name, error=str(e))
            return self._create_fallback_competitor_analysis(startup_name, industry)
    
    async def calculate_tam_sam_som(self, industry: str, target_market: str, geographic_scope: str = "global") -> Dict[str, Any]:
        """Calculate TAM, SAM, and SOM for a market"""
        try:
            logger.info("Calculating TAM/SAM/SOM", industry=industry, target_market=target_market)
            
            # Get market size data
            market_size = await self._get_market_size(industry)
            
            # Calculate TAM (Total Addressable Market)
            tam = market_size.get("total_market_size", 0)
            
            # Calculate SAM (Serviceable Addressable Market) - typically 10-20% of TAM
            sam_percentage = 0.15  # 15% as default
            sam = tam * sam_percentage
            
            # Calculate SOM (Serviceable Obtainable Market) - typically 1-5% of SAM
            som_percentage = 0.03  # 3% as default
            som = sam * som_percentage
            
            result = {
                "tam": tam,
                "sam": sam,
                "som": som,
                "tam_percentage": 100,
                "sam_percentage": sam_percentage * 100,
                "som_percentage": som_percentage * 100,
                "currency": "USD",
                "calculation_date": datetime.utcnow().isoformat()
            }
            
            logger.info("TAM/SAM/SOM calculation completed", 
                       tam=tam, sam=sam, som=som)
            return result
            
        except Exception as e:
            logger.error("TAM/SAM/SOM calculation failed", error=str(e))
            return self._create_fallback_tam_sam_som()
    
    async def _get_market_size(self, industry: str) -> Dict[str, Any]:
        """Get market size data for an industry"""
        # This would typically call external APIs
        # For now, return sample data
        return {
            "total_market_size": 1000000000,  # $1B
            "unit": "USD",
            "year": 2024,
            "source": "sample_data"
        }
    
    async def _get_growth_rate(self, industry: str) -> Dict[str, Any]:
        """Get industry growth rate"""
        return {
            "annual_growth_rate": 0.12,  # 12%
            "compound_annual_growth_rate": 0.15,  # 15%
            "forecast_period": "2024-2029",
            "source": "sample_data"
        }
    
    async def _get_key_players(self, industry: str) -> List[Dict[str, Any]]:
        """Get key players in the industry"""
        return [
            {
                "name": "Sample Company 1",
                "market_share": 0.25,
                "revenue": 250000000,
                "employees": 1000,
                "founded": 2010
            },
            {
                "name": "Sample Company 2",
                "market_share": 0.20,
                "revenue": 200000000,
                "employees": 800,
                "founded": 2012
            }
        ]
    
    async def _get_market_trends(self, industry: str) -> List[str]:
        """Get current market trends"""
        return [
            "Digital transformation acceleration",
            "AI/ML integration",
            "Remote work adoption",
            "Sustainability focus"
        ]
    
    async def _get_regulations(self, industry: str) -> List[str]:
        """Get relevant regulations"""
        return [
            "Data protection regulations",
            "Industry-specific compliance",
            "Environmental regulations"
        ]
    
    async def _get_market_risks(self, industry: str) -> List[str]:
        """Get market risks"""
        return [
            "Economic downturn",
            "Regulatory changes",
            "Technology disruption",
            "Competition intensification"
        ]
    
    async def _find_competitors(self, startup_name: str, industry: str) -> List[Dict[str, Any]]:
        """Find competitors in the market"""
        return [
            {
                "name": "Competitor 1",
                "strengths": ["Strong brand", "Large customer base"],
                "weaknesses": ["Slow innovation", "High costs"],
                "market_position": "leader"
            },
            {
                "name": "Competitor 2",
                "strengths": ["Innovative technology", "Agile development"],
                "weaknesses": ["Limited resources", "Small team"],
                "market_position": "challenger"
            }
        ]
    
    async def _analyze_competitive_landscape(self, competitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the competitive landscape"""
        return {
            "market_concentration": "moderate",
            "barriers_to_entry": "medium",
            "competitive_intensity": "high",
            "key_differentiators": ["technology", "customer_service", "pricing"]
        }
    
    async def _find_differentiation_opportunities(self, competitors: List[Dict[str, Any]]) -> List[str]:
        """Find opportunities for differentiation"""
        return [
            "Superior customer experience",
            "Innovative pricing model",
            "Advanced technology stack",
            "Better market targeting"
        ]
    
    def _create_fallback_market_data(self, industry: str) -> Dict[str, Any]:
        """Create fallback market data when API calls fail"""
        return {
            "industry": industry,
            "timestamp": datetime.utcnow().isoformat(),
            "market_size": {"total_market_size": 1000000000, "unit": "USD"},
            "growth_rate": {"annual_growth_rate": 0.10},
            "key_players": [],
            "trends": ["Sample trend"],
            "regulations": ["Sample regulation"],
            "risks": ["Sample risk"],
            "source": "fallback_data"
        }
    
    def _create_fallback_competitor_analysis(self, startup_name: str, industry: str) -> Dict[str, Any]:
        """Create fallback competitor analysis"""
        return {
            "startup_name": startup_name,
            "industry": industry,
            "timestamp": datetime.utcnow().isoformat(),
            "competitors": [],
            "competitive_landscape": {"market_concentration": "unknown"},
            "differentiation_opportunities": ["Sample opportunity"],
            "source": "fallback_data"
        }
    
    def _create_fallback_tam_sam_som(self) -> Dict[str, Any]:
        """Create fallback TAM/SAM/SOM data"""
        return {
            "tam": 1000000000,
            "sam": 150000000,
            "som": 4500000,
            "tam_percentage": 100,
            "sam_percentage": 15,
            "som_percentage": 3,
            "currency": "USD",
            "calculation_date": datetime.utcnow().isoformat(),
            "source": "fallback_data"
        } 