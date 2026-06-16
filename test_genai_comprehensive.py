#!/usr/bin/env python3
"""
Comprehensive GenAI Lab API Test Suite
Tests all integrated services
"""
import os
import json
import httpx
from langchain_openai import ChatOpenAI
from datetime import datetime

GENAI_BASE_URL = "https://genailab.tcs.in"
GENAI_API_KEY = "sk-ZL8f54qUk4Co3L4iKjt4Qg"
httpx_client = httpx.Client(verify=False)

def test_chat_completion():
    """Test chat completion service"""
    print("\n" + "=" * 70)
    print("TEST 1: Chat Completion")
    print("=" * 70)
    
    try:
        llm = ChatOpenAI(
            base_url=GENAI_BASE_URL,
            model="azure_ai/genailab-maas-DeepSeek-V3-0324",
            api_key=GENAI_API_KEY,
            http_client=httpx_client,
            temperature=0.7,
        )
        
        prompt = "What are the key factors to consider when estimating construction costs for a residential building?"
        print(f"📝 Prompt: {prompt}\n")
        
        response = llm.invoke(prompt)
        print(f"✅ Response:\n{response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


def test_construction_advice():
    """Test construction-specific advice"""
    print("\n" + "=" * 70)
    print("TEST 2: Construction Advice")
    print("=" * 70)
    
    try:
        llm = ChatOpenAI(
            base_url=GENAI_BASE_URL,
            model="azure_ai/genailab-maas-DeepSeek-V3-0324",
            api_key=GENAI_API_KEY,
            http_client=httpx_client,
            temperature=0.5,
        )
        
        prompt = "For a 5000 sq ft residential building with 3 floors, estimate the timeline phases: foundation, structure, roofing, electrical, plumbing, and finishing."
        print(f"📝 Prompt: {prompt}\n")
        
        response = llm.invoke(prompt)
        print(f"✅ Response:\n{response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


def test_design_prompt():
    """Test architectural design prompt generation"""
    print("\n" + "=" * 70)
    print("TEST 3: Architectural Design Prompt")
    print("=" * 70)
    
    try:
        llm = ChatOpenAI(
            base_url=GENAI_BASE_URL,
            model="azure_ai/genailab-maas-DeepSeek-V3-0324",
            api_key=GENAI_API_KEY,
            http_client=httpx_client,
            temperature=0.7,
        )
        
        prompt = """Generate a detailed architectural design prompt for creating professional architectural renderings of a modern residential villa:
        - Total area: 8000 sq ft
        - Floors: 2
        - Material: Concrete and glass
        - Style: Contemporary minimalist
        - Include: 2D floor plans, 3D exterior, 3D interior, and construction blueprint"""
        
        print(f"📝 Prompt: {prompt}\n")
        
        response = llm.invoke(prompt)
        print(f"✅ Response:\n{response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


def test_material_recommendations():
    """Test material recommendation system"""
    print("\n" + "=" * 70)
    print("TEST 4: Material Recommendations")
    print("=" * 70)
    
    try:
        llm = ChatOpenAI(
            base_url=GENAI_BASE_URL,
            model="azure_ai/genailab-maas-DeepSeek-V3-0324",
            api_key=GENAI_API_KEY,
            http_client=httpx_client,
            temperature=0.6,
        )
        
        prompt = "Recommend the best materials for a commercial office building in Mumbai considering climate, durability, cost-effectiveness, and aesthetics. Provide pros and cons for each material type."
        print(f"📝 Prompt: {prompt}\n")
        
        response = llm.invoke(prompt)
        print(f"✅ Response:\n{response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


def test_cost_estimation_logic():
    """Test cost estimation logic"""
    print("\n" + "=" * 70)
    print("TEST 5: Cost Estimation Logic")
    print("=" * 70)
    
    try:
        llm = ChatOpenAI(
            base_url=GENAI_BASE_URL,
            model="azure_ai/genailab-maas-DeepSeek-V3-0324",
            api_key=GENAI_API_KEY,
            http_client=httpx_client,
            temperature=0.5,
        )
        
        prompt = """Calculate estimated cost breakdown for a 10000 sq ft commercial building:
        - Building Type: Commercial office
        - Floors: 5
        - Material: Steel frame with glass facade
        - Location: New York
        
        Provide:
        1. Cost per square foot
        2. Material cost breakdown (percentage)
        3. Labor cost estimate
        4. Equipment and contingency
        5. Timeline estimate"""
        
        print(f"📝 Prompt: {prompt}\n")
        
        response = llm.invoke(prompt)
        print(f"✅ Response:\n{response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("GenAI Lab - Comprehensive API Test Suite")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)
    
    results = {
        "Chat Completion": test_chat_completion(),
        "Construction Advice": test_construction_advice(),
        "Architectural Design": test_design_prompt(),
        "Material Recommendations": test_material_recommendations(),
        "Cost Estimation": test_cost_estimation_logic(),
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
    success = main()
    exit(0 if success else 1)
