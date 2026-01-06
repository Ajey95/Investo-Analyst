# agents/analyst_agent.py
import json
import google.generativeai as genai
from config import MODEL_ANALYST
from protocols.a2a_messaging import AgentPrompts
from core.state_schema import InvestmentMemo
from utils.logger import AgentLogger

class AnalystAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=MODEL_ANALYST,
            generation_config={"response_mime_type": "application/json"}
        )

    def generate_draft(self, context_text: str) -> InvestmentMemo:
        AgentLogger.log("Gemini-Flash", "Generating Investment Memo...")
        """
        Calls Gemini Flash to draft the memo.
        """
        print("⚡ ANALYST: Reading PDF and drafting memo...")
        
        prompt = AgentPrompts.get_analyst_prompt(context_text)
        
        try:
            # Generate content
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            response_json = json.loads(response.text)
            
            # Validate against Pydantic Schema
            memo = InvestmentMemo(**response_json)
            
            print("⚡ ANALYST: Draft complete.")
            AgentLogger.log("Gemini-Flash", "Done.")
            return memo
            
        except Exception as e:
            print(f"❌ ANALYST ERROR: {e}")
            # Return a dummy empty object in case of failure to keep app alive
            return InvestmentMemo(
                company_name="Error", 
                executive_summary="Failed to generate", 
                key_strengths=[], 
                risks=[], 
                verdict="Pass"
            )