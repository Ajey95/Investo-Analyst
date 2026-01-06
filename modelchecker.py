import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()  
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("SDK Version:", genai.__version__)

print("\n=== AVAILABLE MODELS (v1beta) ===")
models = genai.list_models()

for m in models:
    print("-", m.name)