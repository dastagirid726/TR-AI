#!/usr/bin/env python3
"""
Test script for GenAI Lab API integration
"""
import os
import sys
import httpx
from langchain_openai import ChatOpenAI

# Disable SSL verification for testing (use with caution)
httpx_client = httpx.Client(verify=False)

# Configuration
GENAI_BASE_URL = "https://genailab.tcs.in"
GENAI_API_KEY = "sk-ZL8f54qUk4Co3L4iKjt4Qg"
MODEL = "azure_ai/genailab-maas-DeepSeek-V3-0324"

print("=" * 70)
print("GenAI Lab API Connection Test")
print("=" * 70)
print(f"\nConfiguration:")
print(f"  Base URL: {GENAI_BASE_URL}")
print(f"  Model: {MODEL}")
print(f"  API Key: {GENAI_API_KEY[:10]}...{GENAI_API_KEY[-5:]}")

try:
    print(f"\n⏳ Initializing ChatOpenAI client...")
    
    llm = ChatOpenAI(
        base_url=GENAI_BASE_URL,
        model=MODEL,
        api_key=GENAI_API_KEY,
        http_client=httpx_client,
        temperature=0.7,
    )
    
    print("✅ ChatOpenAI client initialized successfully")
    
    print(f"\n⏳ Testing API with message: 'Hi'")
    response = llm.invoke("Hi")
    
    print("✅ API Response Received!")
    print(f"\n📝 Response:")
    print(f"  {response.content}")
    
    print("\n" + "=" * 70)
    print("✅ API Connection Test SUCCESSFUL!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {str(e)}")
    print("\n" + "=" * 70)
    print("❌ API Connection Test FAILED!")
    print("=" * 70)
    sys.exit(1)
