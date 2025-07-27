#!/usr/bin/env python3
"""
Simple script to generate pitch decks using the AI Pitch Deck Generator API
"""

import requests
import json
from typing import Dict, Any

def generate_pitch_deck(startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a pitch deck for a startup
    
    Args:
        startup_data: Dictionary containing startup information
        
    Returns:
        Dictionary containing the generated pitch deck
    """
    url = "http://localhost:8000/api/generate-pitch-deck"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=startup_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating pitch deck: {e}")
        return None

def print_pitch_deck_summary(pitch_deck: Dict[str, Any]):
    """Print a summary of the generated pitch deck"""
    if not pitch_deck:
        print("❌ Failed to generate pitch deck")
        return
    
    print("\n" + "="*60)
    print("🎉 PITCH DECK GENERATED SUCCESSFULLY!")
    print("="*60)
    
    print(f"🚀 Startup: {pitch_deck['startup_name']}")
    print(f"📊 Slides Generated: {len(pitch_deck['slides'])}")
    
    print(f"\n📈 Market Data:")
    market_data = pitch_deck['market_data']
    print(f"   • TAM: ${market_data['market_size']['tam']:,}")
    print(f"   • SAM: ${market_data['market_size']['sam']:,}")
    print(f"   • SOM: ${market_data['market_size']['som']:,}")
    
    print(f"\n💰 Financial Model:")
    financial_model = pitch_deck['financial_model']
    print(f"   • Year 1 Revenue: ${financial_model['revenue_projections']['year_1']:,}")
    print(f"   • Year 3 Revenue: ${financial_model['revenue_projections']['year_3']:,}")
    print(f"   • Valuation: ${financial_model['valuation']['estimated_valuation']:,}")
    
    print(f"\n📋 Generated Slides:")
    for i, slide in enumerate(pitch_deck['slides'], 1):
        print(f"   {i}. {slide['title']}")
    
    print("\n" + "="*60)

def main():
    """Main function to demonstrate pitch deck generation"""
    print("🚀 AI PITCH DECK GENERATOR")
    print("="*40)
    
    # Example 1: Tech Startup
    print("\n🎯 Example 1: Tech Startup")
    tech_startup = {
        "name": "DataFlow Analytics",
        "industry": "SaaS",
        "problem_statement": "Companies struggle to make sense of their data and extract actionable insights. Current solutions are expensive, complex, and require technical expertise.",
        "solution_description": "DataFlow provides an intuitive, AI-powered analytics platform that automatically generates insights and recommendations from any data source.",
        "target_market": "Small to medium businesses across all industries",
        "current_revenue": 150000,
        "team_size": 8
    }
    
    result = generate_pitch_deck(tech_startup)
    print_pitch_deck_summary(result)
    
    # Example 2: Healthcare Startup
    print("\n🎯 Example 2: Healthcare Startup")
    healthcare_startup = {
        "name": "MediTech Solutions",
        "industry": "Healthcare",
        "problem_statement": "Healthcare providers struggle with patient data management, leading to inefficiencies, errors, and poor patient outcomes.",
        "solution_description": "MediTech offers a comprehensive patient management platform that streamlines workflows, reduces errors, and improves patient care.",
        "target_market": "Hospitals, clinics, and healthcare networks",
        "current_revenue": 300000,
        "team_size": 12
    }
    
    result = generate_pitch_deck(healthcare_startup)
    print_pitch_deck_summary(result)
    
    # Interactive mode
    print("\n🎯 Interactive Mode")
    print("Enter your startup details (or press Enter to skip):")
    
    name = input("Startup Name: ").strip()
    if name:
        industry = input("Industry: ").strip()
        problem = input("Problem Statement: ").strip()
        solution = input("Solution Description: ").strip()
        target_market = input("Target Market: ").strip()
        
        try:
            revenue = float(input("Current Revenue ($): ").strip() or "0")
            team_size = int(input("Team Size: ").strip() or "1")
        except ValueError:
            revenue = 0
            team_size = 1
        
        custom_startup = {
            "name": name,
            "industry": industry,
            "problem_statement": problem,
            "solution_description": solution,
            "target_market": target_market,
            "current_revenue": revenue,
            "team_size": team_size
        }
        
        result = generate_pitch_deck(custom_startup)
        print_pitch_deck_summary(result)

if __name__ == "__main__":
    main() 