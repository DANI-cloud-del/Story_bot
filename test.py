import os
from groq import Groq

def test_api_key(api_key):
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        print("✅ API Key is valid!")
        print("Available models:", [m.id for m in models.data])
        return True
    except Exception as e:
        print("❌ API Key is invalid:", e)
        return False

if __name__ == "__main__":
    # Try direct key first
    test_key = "gsk_yourActualKeyHere"  # Replace with your actual key
    print("Testing direct key...")
    direct_result = test_api_key(test_key)
    
    # Then test from environment
    print("\nTesting from environment...")
    env_key = os.getenv("GROQ_API_KEY")
    if env_key:
        test_api_key(env_key)
    else:
        print("No GROQ_API_KEY found in environment variables")
    
    if not direct_result:
        print("\nTroubleshooting steps:")
        print("1. Verify key at https://console.groq.com/api-keys")
        print("2. Check for typos or extra spaces")
        print("3. Ensure account has proper permissions")
        print("4. Try generating a new key")