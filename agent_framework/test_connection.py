import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")
model_name = os.getenv("OPENAI_MODEL_NAME")

print(f"Testing connection to: {base_url}")
print(f"Using model: {model_name}")
print(f"API Key present: {'Yes' if api_key else 'No'}")

if not api_key or not base_url:
    print("Error: Missing API configuration.")
    sys.exit(1)

try:
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=10.0 # Short timeout for quick feedback
    )

    print("Sending test request...")
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": "Hello, are you working?"}],
        max_tokens=10
    )
    
    print("Success! Response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nConnection Failed!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    
    # Diagnosis suggestions
    if "404" in str(e):
        print("\nDiagnosis: 404 Error usually means the Base URL is incorrect.")
        print("Try adding '/v1' to the end of your OPENAI_API_BASE, or removing it if it's already there.")
    elif "timeout" in str(e).lower():
        print("\nDiagnosis: Timeout. Please check your network connection.")
        print("1. Is the URL correct?")
        print("2. Do you have a firewall blocking Python?")
        print("3. Are you using a VPN/Proxy? If so, try disabling it or configuring OPENAI_PROXY.")
