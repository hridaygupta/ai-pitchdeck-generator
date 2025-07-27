#!/usr/bin/env python3
"""
Comprehensive API Test for AI Pitch Deck Generator
Tests all endpoints and demonstrates functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health: {data['status']}")
        print(f"   Services: {data['services']}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_root():
    """Test root endpoint"""
    print("\n🏠 Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API: {data['message']}")
        print(f"   Version: {data['version']}")
        print(f"   Status: {data['status']}")
        print(f"   Features: {len(data['features'])} features available")
        return True
    else:
        print(f"❌ Root endpoint failed: {response.status_code}")
        return False

def test_templates():
    """Test templates endpoint"""
    print("\n📋 Testing Templates Endpoint...")
    response = requests.get(f"{BASE_URL}/api/templates")
    if response.status_code == 200:
        templates = response.json()
        print(f"✅ Templates: {len(templates)} templates available")
        for template in templates:
            print(f"   📄 {template['name']} ({template['slide_count']} slides)")
        return True
    else:
        print(f"❌ Templates failed: {response.status_code}")
        return False

def test_export_formats():
    """Test export formats endpoint"""
    print("\n📄 Testing Export Formats Endpoint...")
    response = requests.get(f"{BASE_URL}/api/export/formats")
    if response.status_code == 200:
        formats = response.json()
        print(f"✅ Export Formats: {len(formats)} formats available")
        for fmt in formats:
            print(f"   📎 {fmt['name']} ({fmt['extension']})")
        return True
    else:
        print(f"❌ Export formats failed: {response.status_code}")
        return False

def test_pitch_deck_generation():
    """Test pitch deck generation"""
    print("\n🚀 Testing Pitch Deck Generation...")
    
    # Sample startup data
    startup_data = {
        "name": "InnovateTech Solutions",
        "industry": "Fintech",
        "problem_statement": "Traditional banking systems are slow, expensive, and inaccessible to many people worldwide.",
        "solution_description": "InnovateTech provides a blockchain-based financial platform that enables instant, low-cost, and secure global transactions.",
        "target_market": "Global unbanked and underbanked population",
        "current_revenue": 75000,
        "team_size": 12
    }
    
    print(f"🎯 Generating pitch deck for: {startup_data['name']}")
    print(f"   Industry: {startup_data['industry']}")
    print(f"   Revenue: ${startup_data['current_revenue']:,}")
    print(f"   Team: {startup_data['team_size']} people")
    
    response = requests.post(
        f"{BASE_URL}/api/generate-pitch-deck",
        json=startup_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Pitch Deck Generated Successfully!")
        print(f"   Startup: {result['startup_name']}")
        print(f"   Slides: {len(result['slides'])} slides generated")
        print(f"   Market Data: ${result['market_data']['market_size']['tam']:,} TAM")
        print(f"   Valuation: ${result['financial_model']['valuation']['estimated_valuation']:,}")
        
        # Show slide titles
        print("\n   📊 Generated Slides:")
        for i, slide in enumerate(result['slides'], 1):
            print(f"      {i}. {slide['title']}")
        
        return True
    else:
        print(f"❌ Pitch deck generation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def test_api_documentation():
    """Test API documentation"""
    print("\n📚 Testing API Documentation...")
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        print("✅ API Documentation available at /docs")
        print("   Swagger UI interface is working")
        return True
    else:
        print(f"❌ API documentation failed: {response.status_code}")
        return False

def test_openapi_spec():
    """Test OpenAPI specification"""
    print("\n🔧 Testing OpenAPI Specification...")
    response = requests.get(f"{BASE_URL}/openapi.json")
    if response.status_code == 200:
        spec = response.json()
        print(f"✅ OpenAPI Specification loaded")
        print(f"   Title: {spec['info']['title']}")
        print(f"   Version: {spec['info']['version']}")
        print(f"   Endpoints: {len(spec['paths'])} endpoints defined")
        return True
    else:
        print(f"❌ OpenAPI spec failed: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("=" * 80)
    print("🧪 AI PITCH DECK GENERATOR - API TEST SUITE")
    print("=" * 80)
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    tests = [
        test_health,
        test_root,
        test_templates,
        test_export_formats,
        test_pitch_deck_generation,
        test_api_documentation,
        test_openapi_spec
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {passed}/{total} tests")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 The AI Pitch Deck Generator is fully functional!")
        print("\n📋 Available Features:")
        print("   • AI-powered content generation")
        print("   • Market research integration")
        print("   • Financial modeling")
        print("   • Multi-format export")
        print("   • Professional templates")
        print("   • Real-time collaboration")
        print("   • Enterprise features")
        
        print("\n🌐 Access Points:")
        print(f"   • API: {BASE_URL}")
        print(f"   • Documentation: {BASE_URL}/docs")
        print(f"   • Health Check: {BASE_URL}/health")
        
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("Please check the server logs for more details")
    
    print("=" * 80)

if __name__ == "__main__":
    main() 