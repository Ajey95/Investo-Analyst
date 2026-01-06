# # config.py
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load .env file
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

# # Configure the global SDK
# genai.configure(api_key=GOOGLE_API_KEY)

# # Model Definitions
# # We use 1.5 Flash for speed (Analyst) and 1.5 Pro for reasoning (Critic)
# MODEL_ANALYST = "gemini-1.5-flash"
# MODEL_CRITIC = "gemini-1.5-pro"
# config.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

# Configure the global SDK
genai.configure(api_key=GOOGLE_API_KEY)

# --- MODEL SELECTION ---
# We use the "2.0 Flash" family to avoid Rate Limit errors while keeping high intelligence.

# 1. THE ANALYST (Generator)
# 'gemini-2.0-flash-lite' is optimized for speed and high-throughput. Perfect for drafting.
MODEL_ANALYST = "gemini-2.5-flash"

# 2. THE CRITIC (Auditor)
# 'gemini-2.0-flash' has "Pro-level" reasoning capabilities but runs at Flash speeds/limits.
MODEL_CRITIC = "gemini-2.5-flash"

# --- DEBUGGING (Optional: Verify key is loaded) ---
# print(f"DEBUG: Config loaded. Key length: {len(GOOGLE_API_KEY)}")