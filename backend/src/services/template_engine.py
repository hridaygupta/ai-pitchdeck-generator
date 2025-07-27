"""
Template engine service for pitch deck templates
"""
import os
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = structlog.get_logger()

class TemplateEngine:
    """Template engine for pitch deck generation"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load available templates"""
        return {
            "saas": {
                "name": "SaaS Startup Template",
                "slides": [
                    "title", "problem", "solution", "market_opportunity",
                    "business_model", "traction", "competition", "team",
                    "financials", "funding_ask"
                ],
                "design": {
                    "primary_color": "#2563eb",
                    "secondary_color": "#64748b",
                    "font_family": "Inter",
                    "layout": "modern"
                }
            },
            "fintech": {
                "name": "Fintech Startup Template",
                "slides": [
                    "title", "problem", "solution", "market_opportunity",
                    "business_model", "traction", "competition", "team",
                    "financials", "funding_ask", "regulatory_compliance"
                ],
                "design": {
                    "primary_color": "#059669",
                    "secondary_color": "#374151",
                    "font_family": "Inter",
                    "layout": "professional"
                }
            },
            "healthcare": {
                "name": "Healthcare Startup Template",
                "slides": [
                    "title", "problem", "solution", "market_opportunity",
                    "business_model", "traction", "competition", "team",
                    "financials", "funding_ask", "clinical_evidence"
                ],
                "design": {
                    "primary_color": "#dc2626",
                    "secondary_color": "#6b7280",
                    "font_family": "Inter",
                    "layout": "medical"
                }
            }
        }
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific template"""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates"""
        return [
            {
                "id": template_id,
                "name": template["name"],
                "slide_count": len(template["slides"]),
                "design": template["design"]
            }
            for template_id, template in self.templates.items()
        ]
    
    def apply_template(self, template_id: str, startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a template to startup data"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        return {
            "template_id": template_id,
            "template_name": template["name"],
            "slides": template["slides"],
            "design": template["design"],
            "startup_data": startup_data,
            "applied_at": datetime.utcnow().isoformat()
        } 