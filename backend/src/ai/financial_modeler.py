"""
Financial modeling module for startup financial projections
"""
import os
import asyncio
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = structlog.get_logger()

class FinancialModeler:
    """Financial modeling and projections for startups"""
    
    def __init__(self):
        self.default_assumptions = {
            "revenue_growth_rate": 0.20,  # 20% monthly growth
            "customer_acquisition_cost": 100,
            "customer_lifetime_value": 500,
            "churn_rate": 0.05,  # 5% monthly churn
            "gross_margin": 0.70,  # 70% gross margin
            "operating_margin": 0.20,  # 20% operating margin
            "burn_rate": 50000  # $50k monthly burn
        }
    
    async def create_financial_model(self, startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive financial model for a startup"""
        try:
            logger.info("Creating financial model", startup_name=startup_data.get("name"))
            
            # Extract key metrics from startup data
            current_revenue = startup_data.get("current_revenue", 0)
            customer_count = startup_data.get("customer_count", 0)
            team_size = startup_data.get("team_size", 1)
            funding_stage = startup_data.get("funding_stage", "seed")
            
            # Generate projections
            revenue_projections = await self._project_revenue(current_revenue, customer_count, funding_stage)
            cost_projections = await self._project_costs(team_size, funding_stage)
            cash_flow_projections = await self._project_cash_flow(revenue_projections, cost_projections)
            unit_economics = await self._calculate_unit_economics(startup_data)
            valuation_model = await self._calculate_valuation(revenue_projections, funding_stage)
            
            financial_model = {
                "startup_name": startup_data.get("name"),
                "created_at": datetime.utcnow().isoformat(),
                "projection_period": "36 months",
                "revenue_projections": revenue_projections,
                "cost_projections": cost_projections,
                "cash_flow_projections": cash_flow_projections,
                "unit_economics": unit_economics,
                "valuation_model": valuation_model,
                "key_metrics": await self._calculate_key_metrics(revenue_projections, cost_projections),
                "scenarios": await self._create_scenarios(startup_data)
            }
            
            logger.info("Financial model created successfully", startup_name=startup_data.get("name"))
            return financial_model
            
        except Exception as e:
            logger.error("Financial model creation failed", error=str(e))
            return self._create_fallback_financial_model(startup_data)
    
    async def _project_revenue(self, current_revenue: float, customer_count: int, funding_stage: str) -> Dict[str, Any]:
        """Project revenue growth over 36 months"""
        months = 36
        revenue_data = []
        
        # Adjust growth rate based on funding stage
        growth_rates = {
            "seed": 0.15,
            "series_a": 0.25,
            "series_b": 0.30,
            "series_c": 0.20
        }
        growth_rate = growth_rates.get(funding_stage, 0.20)
        
        monthly_revenue = current_revenue
        for month in range(1, months + 1):
            # Apply growth rate with some variability
            growth_multiplier = 1 + growth_rate + np.random.normal(0, 0.05)
            monthly_revenue *= max(0.8, growth_multiplier)  # Ensure positive growth
            
            revenue_data.append({
                "month": month,
                "revenue": round(monthly_revenue, 2),
                "growth_rate": growth_rate,
                "cumulative_revenue": round(sum([r["revenue"] for r in revenue_data]) + monthly_revenue, 2)
            })
        
        return {
            "monthly_revenue": revenue_data,
            "annual_revenue": [sum([r["revenue"] for r in revenue_data[i:i+12]]) for i in range(0, len(revenue_data), 12)],
            "total_revenue_36_months": sum([r["revenue"] for r in revenue_data]),
            "average_monthly_growth": growth_rate
        }
    
    async def _project_costs(self, team_size: int, funding_stage: str) -> Dict[str, Any]:
        """Project costs over 36 months"""
        months = 36
        cost_data = []
        
        # Base costs per employee
        base_salary = 8000  # $8k per month per employee
        overhead_per_employee = 2000  # $2k overhead per employee
        
        # Team growth assumptions
        team_growth_rates = {
            "seed": 0.10,  # 10% monthly team growth
            "series_a": 0.15,
            "series_b": 0.20,
            "series_c": 0.15
        }
        team_growth = team_growth_rates.get(funding_stage, 0.10)
        
        current_team_size = team_size
        for month in range(1, months + 1):
            # Grow team
            current_team_size *= (1 + team_growth)
            current_team_size = min(current_team_size, 100)  # Cap at 100 employees
            
            # Calculate costs
            personnel_costs = current_team_size * base_salary
            overhead_costs = current_team_size * overhead_per_employee
            marketing_costs = personnel_costs * 0.3  # 30% of personnel costs
            other_costs = personnel_costs * 0.2  # 20% of personnel costs
            
            total_costs = personnel_costs + overhead_costs + marketing_costs + other_costs
            
            cost_data.append({
                "month": month,
                "team_size": round(current_team_size, 1),
                "personnel_costs": round(personnel_costs, 2),
                "overhead_costs": round(overhead_costs, 2),
                "marketing_costs": round(marketing_costs, 2),
                "other_costs": round(other_costs, 2),
                "total_costs": round(total_costs, 2)
            })
        
        return {
            "monthly_costs": cost_data,
            "annual_costs": [sum([c["total_costs"] for c in cost_data[i:i+12]]) for i in range(0, len(cost_data), 12)],
            "total_costs_36_months": sum([c["total_costs"] for c in cost_data]),
            "average_monthly_burn": sum([c["total_costs"] for c in cost_data]) / len(cost_data)
        }
    
    async def _project_cash_flow(self, revenue_projections: Dict[str, Any], cost_projections: Dict[str, Any]) -> Dict[str, Any]:
        """Project cash flow over 36 months"""
        months = 36
        cash_flow_data = []
        
        starting_cash = 1000000  # $1M starting cash
        current_cash = starting_cash
        
        for month in range(1, months + 1):
            revenue = revenue_projections["monthly_revenue"][month-1]["revenue"]
            costs = cost_projections["monthly_costs"][month-1]["total_costs"]
            
            net_cash_flow = revenue - costs
            current_cash += net_cash_flow
            
            cash_flow_data.append({
                "month": month,
                "revenue": revenue,
                "costs": costs,
                "net_cash_flow": round(net_cash_flow, 2),
                "cumulative_cash": round(current_cash, 2),
                "runway_months": round(current_cash / costs, 1) if costs > 0 else float('inf')
            })
        
        return {
            "monthly_cash_flow": cash_flow_data,
            "starting_cash": starting_cash,
            "ending_cash": current_cash,
            "total_net_cash_flow": current_cash - starting_cash,
            "average_monthly_cash_flow": sum([cf["net_cash_flow"] for cf in cash_flow_data]) / len(cash_flow_data)
        }
    
    async def _calculate_unit_economics(self, startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate unit economics"""
        current_revenue = startup_data.get("current_revenue", 0)
        customer_count = startup_data.get("customer_count", 1)
        
        # Calculate key metrics
        average_revenue_per_user = current_revenue / customer_count if customer_count > 0 else 0
        customer_acquisition_cost = self.default_assumptions["customer_acquisition_cost"]
        customer_lifetime_value = self.default_assumptions["customer_lifetime_value"]
        churn_rate = self.default_assumptions["churn_rate"]
        
        # Calculate LTV/CAC ratio
        ltv_cac_ratio = customer_lifetime_value / customer_acquisition_cost if customer_acquisition_cost > 0 else 0
        
        # Calculate payback period
        payback_period = customer_acquisition_cost / average_revenue_per_user if average_revenue_per_user > 0 else float('inf')
        
        return {
            "average_revenue_per_user": round(average_revenue_per_user, 2),
            "customer_acquisition_cost": customer_acquisition_cost,
            "customer_lifetime_value": customer_lifetime_value,
            "churn_rate": churn_rate,
            "ltv_cac_ratio": round(ltv_cac_ratio, 2),
            "payback_period_months": round(payback_period, 1),
            "gross_margin": self.default_assumptions["gross_margin"],
            "contribution_margin": round(average_revenue_per_user * self.default_assumptions["gross_margin"] - customer_acquisition_cost, 2)
        }
    
    async def _calculate_valuation(self, revenue_projections: Dict[str, Any], funding_stage: str) -> Dict[str, Any]:
        """Calculate startup valuation"""
        # Get projected annual revenue
        annual_revenue = revenue_projections["annual_revenue"][2] if len(revenue_projections["annual_revenue"]) > 2 else revenue_projections["monthly_revenue"][-1]["revenue"] * 12
        
        # Valuation multiples based on funding stage
        valuation_multiples = {
            "seed": 5,  # 5x revenue
            "series_a": 8,
            "series_b": 10,
            "series_c": 12
        }
        multiple = valuation_multiples.get(funding_stage, 8)
        
        valuation = annual_revenue * multiple
        
        return {
            "projected_annual_revenue": round(annual_revenue, 2),
            "valuation_multiple": multiple,
            "estimated_valuation": round(valuation, 2),
            "valuation_date": datetime.utcnow().isoformat(),
            "methodology": "Revenue multiple"
        }
    
    async def _calculate_key_metrics(self, revenue_projections: Dict[str, Any], cost_projections: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate key financial metrics"""
        total_revenue = revenue_projections["total_revenue_36_months"]
        total_costs = cost_projections["total_costs_36_months"]
        average_monthly_revenue = total_revenue / 36
        average_monthly_costs = total_costs / 36
        
        return {
            "total_revenue_36_months": round(total_revenue, 2),
            "total_costs_36_months": round(total_costs, 2),
            "net_profit_36_months": round(total_revenue - total_costs, 2),
            "average_monthly_revenue": round(average_monthly_revenue, 2),
            "average_monthly_costs": round(average_monthly_costs, 2),
            "profit_margin": round((total_revenue - total_costs) / total_revenue * 100, 2) if total_revenue > 0 else 0,
            "revenue_growth_rate": revenue_projections["average_monthly_growth"],
            "burn_rate": round(average_monthly_costs, 2)
        }
    
    async def _create_scenarios(self, startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create different financial scenarios"""
        scenarios = {}
        
        # Base case
        scenarios["base_case"] = await self.create_financial_model(startup_data)
        
        # Optimistic case (20% better growth)
        optimistic_data = startup_data.copy()
        optimistic_data["current_revenue"] = startup_data.get("current_revenue", 0) * 1.2
        scenarios["optimistic"] = await self.create_financial_model(optimistic_data)
        
        # Pessimistic case (20% worse growth)
        pessimistic_data = startup_data.copy()
        pessimistic_data["current_revenue"] = startup_data.get("current_revenue", 0) * 0.8
        scenarios["pessimistic"] = await self.create_financial_model(pessimistic_data)
        
        return scenarios
    
    def _create_fallback_financial_model(self, startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback financial model when calculations fail"""
        return {
            "startup_name": startup_data.get("name", "Unknown"),
            "created_at": datetime.utcnow().isoformat(),
            "projection_period": "36 months",
            "revenue_projections": {"total_revenue_36_months": 0},
            "cost_projections": {"total_costs_36_months": 0},
            "cash_flow_projections": {"total_net_cash_flow": 0},
            "unit_economics": {"ltv_cac_ratio": 0},
            "valuation_model": {"estimated_valuation": 0},
            "key_metrics": {"profit_margin": 0},
            "scenarios": {},
            "source": "fallback_data"
        } 