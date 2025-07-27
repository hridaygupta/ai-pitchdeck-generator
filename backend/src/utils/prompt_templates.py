from typing import Dict, Any
from ..models.slide import SlideType
from ..models.startup import IndustryType

# Industry-specific prompt templates
INDUSTRY_PROMPTS = {
    IndustryType.SAAS: {
        "tone": "professional and technical",
        "focus": "scalability, recurring revenue, and customer acquisition",
        "metrics": "MRR, CAC, LTV, churn rate"
    },
    IndustryType.FINTECH: {
        "tone": "trustworthy and innovative",
        "focus": "compliance, security, and market disruption",
        "metrics": "transaction volume, user growth, regulatory compliance"
    },
    IndustryType.HEALTHCARE: {
        "tone": "compassionate and evidence-based",
        "focus": "patient outcomes, regulatory approval, and clinical validation",
        "metrics": "patient outcomes, FDA approvals, clinical trials"
    },
    IndustryType.ECOMMERCE: {
        "tone": "customer-focused and growth-oriented",
        "focus": "customer experience, logistics, and market expansion",
        "metrics": "GMV, conversion rate, customer lifetime value"
    },
    IndustryType.AI_ML: {
        "tone": "innovative and forward-thinking",
        "focus": "technology differentiation, data moats, and AI capabilities",
        "metrics": "model accuracy, data quality, computational efficiency"
    },
    IndustryType.BIOTECH: {
        "tone": "scientific and breakthrough-oriented",
        "focus": "clinical trials, IP protection, and regulatory pathways",
        "metrics": "clinical trial phases, patent portfolio, FDA milestones"
    }
}

def get_prompt_template(slide_type: SlideType, industry: IndustryType) -> str:
    """Get industry-specific prompt template for slide type"""
    
    industry_config = INDUSTRY_PROMPTS.get(industry, INDUSTRY_PROMPTS[IndustryType.SAAS])
    
    base_prompts = {
        SlideType.TITLE: f"""
Create a compelling title slide for a {industry.value} startup pitch deck.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Company: {{company_name}}
Tagline: {{tagline}}

Generate a JSON response with:
- headline: Compelling main title
- subheadline: Supporting subtitle
- presenter_info: Presenter details
""",
        
        SlideType.PROBLEM: f"""
Create a problem slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Problem Statement: {{problem_statement}}
Target Market: {{target_market}}

Generate a JSON response with:
- problem_statement: Clear problem description
- pain_points: List of 3-5 key pain points
- market_size_impact: Market impact of the problem
- urgency: Why this problem needs solving now
""",
        
        SlideType.SOLUTION: f"""
Create a solution slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Solution: {{solution_description}}
Value Proposition: {{unique_value_proposition}}

Generate a JSON response with:
- solution_overview: Clear solution description
- key_features: List of 3-5 key features
- unique_advantages: Competitive advantages
- value_proposition: Clear value proposition
""",
        
        SlideType.MARKET_OPPORTUNITY: f"""
Create a market opportunity slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

TAM: ${{market_size_tam}}
SAM: ${{market_size_sam}}
SOM: ${{market_size_som}}
Growth Rate: {{market_growth_rate}}%

Generate a JSON response with:
- market_overview: Market description
- growth_drivers: List of 3-5 growth drivers
- market_timing: Why now is the right time
""",
        
        SlideType.BUSINESS_MODEL: f"""
Create a business model slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Revenue Model: {{revenue_model}}
Current Revenue: ${{current_revenue}}

Generate a JSON response with:
- revenue_streams: List of revenue streams
- pricing_strategy: Pricing approach
- customer_segments: Target customer segments
- cost_structure: Key cost components
""",
        
        SlideType.TRACTION: f"""
Create a traction slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Customers: {{customer_count}}
Users: {{user_count}}
Growth Rate: {{growth_rate}}%
Achievements: {{achievements}}

Generate a JSON response with:
- key_metrics: List of key performance metrics
- achievements: List of major achievements
- growth_trajectory: Growth story
- customer_testimonials: Customer feedback highlights
""",
        
        SlideType.COMPETITION: f"""
Create a competitive landscape slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Competitors: {{competitors}}
Competitive Advantages: {{competitive_advantages}}

Generate a JSON response with:
- competitor_analysis: List of key competitors
- competitive_advantages: List of advantages
- market_positioning: Market position
- differentiation: Key differentiators
""",
        
        SlideType.TEAM: f"""
Create a team slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Team Size: {{team_size}}
Experience: {{team_experience}}
Key Members: {{team_members}}

Generate a JSON response with:
- team_overview: Team summary
- key_members: List of key team members
- expertise_areas: Areas of expertise
- advisors: Advisory board members
""",
        
        SlideType.FINANCIALS: f"""
Create a financial projections slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Current Revenue: ${{current_revenue}}
Burn Rate: ${{burn_rate}}/month
Runway: {{runway_months}} months
Projections: {{financial_projections}}

Generate a JSON response with:
- revenue_projections: 3-5 year revenue projections
- unit_economics: Key unit economics
- funding_utilization: How funding will be used
- path_to_profitability: Path to profitability
""",
        
        SlideType.FUNDING_ASK: f"""
Create a funding ask slide for a {industry.value} startup.
Tone: {industry_config['tone']}
Focus: {industry_config['focus']}

Funding Ask: ${{funding_ask}}
Use of Funds: {{use_of_funds}}
Valuation: ${{current_valuation}}

Generate a JSON response with:
- funding_amount: Clear funding request
- use_of_funds: List of funding allocation
- valuation: Company valuation
- milestones: Key milestones to be achieved
"""
    }
    
    return base_prompts.get(slide_type, base_prompts[SlideType.TITLE])

def get_industry_specific_metrics(industry: IndustryType) -> Dict[str, Any]:
    """Get industry-specific metrics and KPIs"""
    metrics = {
        IndustryType.SAAS: {
            "primary_metrics": ["MRR", "ARR", "CAC", "LTV", "Churn Rate"],
            "secondary_metrics": ["NPS", "Feature Adoption", "Customer Satisfaction"],
            "growth_metrics": ["Revenue Growth", "Customer Growth", "Expansion Revenue"]
        },
        IndustryType.FINTECH: {
            "primary_metrics": ["Transaction Volume", "User Growth", "Revenue per User"],
            "secondary_metrics": ["Regulatory Compliance", "Security Score", "Customer Trust"],
            "growth_metrics": ["Market Penetration", "Geographic Expansion", "Product Adoption"]
        },
        IndustryType.HEALTHCARE: {
            "primary_metrics": ["Patient Outcomes", "Clinical Efficacy", "Regulatory Milestones"],
            "secondary_metrics": ["Provider Adoption", "Patient Satisfaction", "Cost Savings"],
            "growth_metrics": ["Clinical Trial Progress", "Market Access", "Reimbursement"]
        },
        IndustryType.ECOMMERCE: {
            "primary_metrics": ["GMV", "Conversion Rate", "Customer Lifetime Value"],
            "secondary_metrics": ["Customer Satisfaction", "Return Rate", "Average Order Value"],
            "growth_metrics": ["Market Share", "Geographic Expansion", "Category Expansion"]
        },
        IndustryType.AI_ML: {
            "primary_metrics": ["Model Accuracy", "Data Quality", "Computational Efficiency"],
            "secondary_metrics": ["API Usage", "Model Performance", "User Adoption"],
            "growth_metrics": ["Data Growth", "Model Improvements", "Market Applications"]
        },
        IndustryType.BIOTECH: {
            "primary_metrics": ["Clinical Trial Phases", "Patent Portfolio", "FDA Milestones"],
            "secondary_metrics": ["Research Publications", "Academic Partnerships", "Industry Collaborations"],
            "growth_metrics": ["Pipeline Development", "Regulatory Progress", "Market Access"]
        }
    }
    
    return metrics.get(industry, metrics[IndustryType.SAAS])

def get_industry_specific_competitors(industry: IndustryType) -> Dict[str, Any]:
    """Get industry-specific competitor analysis framework"""
    frameworks = {
        IndustryType.SAAS: {
            "competition_types": ["Direct Competitors", "Indirect Competitors", "Legacy Solutions"],
            "evaluation_criteria": ["Feature Set", "Pricing", "Ease of Use", "Integration Capabilities"],
            "differentiation_factors": ["Technology Stack", "Customer Experience", "Pricing Model"]
        },
        IndustryType.FINTECH: {
            "competition_types": ["Traditional Banks", "Fintech Startups", "Tech Giants"],
            "evaluation_criteria": ["Security", "Compliance", "User Experience", "Cost"],
            "differentiation_factors": ["Regulatory Advantage", "Technology Innovation", "Customer Trust"]
        },
        IndustryType.HEALTHCARE: {
            "competition_types": ["Pharmaceutical Companies", "Medical Device Companies", "Digital Health Startups"],
            "evaluation_criteria": ["Clinical Efficacy", "Safety Profile", "Cost Effectiveness", "Ease of Use"],
            "differentiation_factors": ["Clinical Data", "Regulatory Status", "Market Access"]
        },
        IndustryType.ECOMMERCE: {
            "competition_types": ["Marketplace Platforms", "Direct Competitors", "Brick-and-Mortar Retailers"],
            "evaluation_criteria": ["Product Selection", "Pricing", "Delivery Speed", "Customer Service"],
            "differentiation_factors": ["Unique Products", "Customer Experience", "Supply Chain"]
        },
        IndustryType.AI_ML: {
            "competition_types": ["AI Research Labs", "Tech Companies", "AI Startups"],
            "evaluation_criteria": ["Model Performance", "Data Quality", "Scalability", "Cost"],
            "differentiation_factors": ["Proprietary Algorithms", "Data Access", "Domain Expertise"]
        },
        IndustryType.BIOTECH: {
            "competition_types": ["Pharmaceutical Companies", "Biotech Startups", "Academic Institutions"],
            "evaluation_criteria": ["Clinical Pipeline", "IP Portfolio", "Regulatory Progress", "Market Access"],
            "differentiation_factors": ["Novel Technology", "Clinical Data", "Regulatory Strategy"]
        }
    }
    
    return frameworks.get(industry, frameworks[IndustryType.SAAS])

def get_industry_specific_risks(industry: IndustryType) -> Dict[str, Any]:
    """Get industry-specific risk factors"""
    risks = {
        IndustryType.SAAS: {
            "market_risks": ["Market Saturation", "Economic Downturn", "Technology Changes"],
            "operational_risks": ["Customer Churn", "Technical Debt", "Scaling Challenges"],
            "competitive_risks": ["New Entrants", "Feature Parity", "Price Wars"]
        },
        IndustryType.FINTECH: {
            "market_risks": ["Regulatory Changes", "Economic Volatility", "Cybersecurity Threats"],
            "operational_risks": ["Compliance Failures", "System Outages", "Data Breaches"],
            "competitive_risks": ["Bank Competition", "Tech Giant Entry", "Regulatory Barriers"]
        },
        IndustryType.HEALTHCARE: {
            "market_risks": ["Regulatory Delays", "Reimbursement Changes", "Clinical Trial Failures"],
            "operational_risks": ["Manufacturing Issues", "Quality Control", "Supply Chain Disruptions"],
            "competitive_risks": ["Patent Expiration", "Generic Competition", "New Technologies"]
        },
        IndustryType.ECOMMERCE: {
            "market_risks": ["Economic Recession", "Consumer Behavior Changes", "Supply Chain Disruptions"],
            "operational_risks": ["Logistics Failures", "Inventory Management", "Customer Service"],
            "competitive_risks": ["Amazon Competition", "Price Wars", "New Marketplaces"]
        },
        IndustryType.AI_ML: {
            "market_risks": ["Technology Changes", "Regulatory Concerns", "Ethical Issues"],
            "operational_risks": ["Data Quality", "Model Drift", "Computational Costs"],
            "competitive_risks": ["Open Source Alternatives", "Tech Giant Competition", "Talent Shortage"]
        },
        IndustryType.BIOTECH: {
            "market_risks": ["Clinical Trial Failures", "Regulatory Rejection", "Market Access Issues"],
            "operational_risks": ["Manufacturing Scale-up", "Quality Control", "Supply Chain"],
            "competitive_risks": ["Patent Challenges", "Generic Competition", "New Technologies"]
        }
    }
    
    return risks.get(industry, risks[IndustryType.SAAS])

def get_industry_specific_opportunities(industry: IndustryType) -> Dict[str, Any]:
    """Get industry-specific growth opportunities"""
    opportunities = {
        IndustryType.SAAS: {
            "market_expansion": ["Geographic Expansion", "Vertical Expansion", "Product Line Extension"],
            "technology_opportunities": ["AI Integration", "Mobile-First", "API Ecosystem"],
            "business_model_opportunities": ["Freemium to Premium", "Marketplace", "Enterprise Sales"]
        },
        IndustryType.FINTECH: {
            "market_expansion": ["Unbanked Markets", "SME Banking", "Wealth Management"],
            "technology_opportunities": ["Blockchain", "AI/ML", "Open Banking"],
            "business_model_opportunities": ["B2B2C", "Embedded Finance", "Regulatory Arbitrage"]
        },
        IndustryType.HEALTHCARE: {
            "market_expansion": ["Emerging Markets", "Preventive Care", "Digital Therapeutics"],
            "technology_opportunities": ["AI Diagnostics", "Telemedicine", "Wearable Technology"],
            "business_model_opportunities": ["Value-Based Care", "Direct-to-Consumer", "Pharma Partnerships"]
        },
        IndustryType.ECOMMERCE: {
            "market_expansion": ["International Markets", "B2B Commerce", "Social Commerce"],
            "technology_opportunities": ["AR/VR", "AI Personalization", "Voice Commerce"],
            "business_model_opportunities": ["Subscription Models", "Marketplace", "D2C Brands"]
        },
        IndustryType.AI_ML: {
            "market_expansion": ["Industry Applications", "Geographic Expansion", "Use Case Diversification"],
            "technology_opportunities": ["Edge AI", "Federated Learning", "AutoML"],
            "business_model_opportunities": ["API-as-a-Service", "Platform-as-a-Service", "Consulting"]
        },
        IndustryType.BIOTECH: {
            "market_expansion": ["Orphan Diseases", "Emerging Markets", "Preventive Medicine"],
            "technology_opportunities": ["Gene Therapy", "Cell Therapy", "Digital Biomarkers"],
            "business_model_opportunities": ["Licensing", "Co-Development", "Acquisition"]
        }
    }
    
    return opportunities.get(industry, opportunities[IndustryType.SAAS]) 