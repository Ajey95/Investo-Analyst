# agents/critic_agent.py
import json
import google.generativeai as genai
from config import MODEL_CRITIC
from protocols.a2a_messaging import AgentPrompts
from core.state_schema import AuditResult, InvestmentMemo
from utils.logger import AgentLogger
class CriticAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=MODEL_CRITIC,
            generation_config={"response_mime_type": "application/json"}
        )

    def critique_draft(self, context_text: str, draft: InvestmentMemo) -> AuditResult:
        AgentLogger.log("Gemini-Pro", "Reading source document vs draft...")
        """
        Calls Gemini Pro to audit the draft.
        """
        print("🧐 CRITIC: Reviewing draft against source...")
        
        # Convert the Pydantic object to a JSON string for the prompt
        draft_json_str = draft.model_dump_json()
        
        prompt = AgentPrompts.get_critic_prompt(context_text, draft_json_str)
        
        try:
            response = self.model.generate_content(prompt)
            
            response_json = json.loads(response.text)
            
            # Validate against Pydantic Schema
            audit = AuditResult(**response_json)
            
            print(f"🧐 CRITIC: Review complete. Verified: {audit.is_verified}")
            return audit

        except Exception as e:
            print(f"❌ CRITIC ERROR: {e}")
            # Fail safe: Default to not verified if error occurs
            return AuditResult(is_verified=False, feedback="System Error during critique", score=0)