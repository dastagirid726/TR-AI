#!/usr/bin/env python3
"""
Backend Service Integration Test
Tests the FastAPI services with GenAI Lab API
"""
import asyncio
import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.cost_estimation import CostEstimationService
from app.services.design_generator import DesignGeneratorService
from app.services.timeline_predictor import TimelinePredictorService
from app.services.ai_chatbot import AIChatbotService

async def test_cost_service():
    """Test cost estimation service"""
    print("\n" + "=" * 70)
    print("TEST 1: Cost Estimation Service")
    print("=" * 70)
    
    try:
        service = CostEstimationService()
        
        request_data = {
            "construction_area": 5000,
            "building_type": "residential",
            "floors": 2,
            "material_type": "concrete",
            "location": "Mumbai"
        }
        
        print(f"📝 Request: {request_data}")
        result = await service.estimate_cost(request_data)
        print(f"✅ Cost Estimation Result:")
        print(f"   Estimated Cost: ₹{result.get('estimated_cost', 'N/A')}")
        print(f"   Cost per Sq Ft: ₹{result.get('cost_per_sqft', 'N/A')}")
        print(f"   Confidence: {result.get('confidence_score', 'N/A')}%")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


async def test_timeline_service():
    """Test timeline prediction service"""
    print("\n" + "=" * 70)
    print("TEST 2: Timeline Prediction Service")
    print("=" * 70)
    
    try:
        service = TimelinePredictorService()
        
        request_data = {
            "building_type": "residential",
            "construction_area": 5000,
            "floors": 3,
            "material_type": "concrete",
            "complexity": "medium"
        }
        
        print(f"📝 Request: {request_data}")
        result = await service.predict_timeline(request_data)
        print(f"✅ Timeline Result:")
        print(f"   Total Days: {result['total_days']}")
        print(f"   Start Date: {result['start_date']}")
        print(f"   End Date: {result['end_date']}")
        print(f"   Phases: {len(result['phases'])} phases")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


async def test_chatbot_service():
    """Test chatbot service"""
    print("\n" + "=" * 70)
    print("TEST 3: Chatbot Service")
    print("=" * 70)
    
    try:
        service = AIChatbotService()
        
        message = "What materials would you recommend for a residential building?"
        history = []
        
        print(f"📝 Message: {message}")
        response = await service.send_message(message, history)
        print(f"✅ Chatbot Response:")
        print(f"   {response['content'][:200]}...")
        print(f"   Suggestions: {len(response['suggestions'])} follow-up questions")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


async def test_design_service():
    """Test design generation service"""
    print("\n" + "=" * 70)
    print("TEST 4: Design Generation Service")
    print("=" * 70)
    
    try:
        service = DesignGeneratorService()
        
        request_data = {
            "building_type": "residential",
            "construction_area": 5000,
            "floors": 2,
            "design_style": "modern",
            "material_type": "concrete"
        }
        
        print(f"📝 Request: {request_data}")
        result = await service.generate_design(request_data)
        print(f"✅ Design Generation Result:")
        print(f"   Has floor_plan_2d: {'floor_plan_2d' in result}")
        print(f"   Has exterior_render_3d: {'exterior_render_3d' in result}")
        print(f"   Has interior_render_3d: {'interior_render_3d' in result}")
        print(f"   Has construction_blueprint: {'construction_blueprint' in result}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


async def main():
    """Run all service tests"""
    print("\n" + "=" * 70)
    print("Backend Service Integration Test Suite")
    print("=" * 70)
    
    results = {
        "Cost Estimation": await test_cost_service(),
        "Timeline Prediction": await test_timeline_service(),
        "Chatbot": await test_chatbot_service(),
        "Design Generation": await test_design_service(),
    }
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("\n" + "-" * 70)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
