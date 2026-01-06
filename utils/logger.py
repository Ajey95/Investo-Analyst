# utils/logger.py
import datetime
import sys

class AgentLogger:
    # ANSI Color Codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def log(component: str, message: str, type: str = "INFO"):
        """
        Format: > [TIME] [COMPONENT] MESSAGE
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Auto-color based on Component Name
        color = AgentLogger.RESET
        if "ADK" in component:
            color = AgentLogger.CYAN
        elif "Gemini" in component:
            color = AgentLogger.BLUE
        elif "A2A" in component:
            color = AgentLogger.YELLOW
        elif "System" in component:
            color = AgentLogger.GREEN + AgentLogger.BOLD
        
        # Icon mapping for specific types
        icon = ""
        if "ALERT" in message: icon = "🟡 "
        if "REJECTED" in message: icon = "❌ "
        if "APPROVED" in message: icon = "✅ "
        if "TRANSITION" in message: icon = "🚀 "

        formatted_msg = f"{color}> [{timestamp}] [{component}] {icon}{message}{AgentLogger.RESET}"
        
        # Print to console immediately
        print(formatted_msg)
        sys.stdout.flush()

# Example Test (You can run this file directly to test colors):
# if __name__ == "__main__":
#     AgentLogger.log("ADK-Orchestrator", "State Transition: INIT -> DRAFTING")
#     AgentLogger.log("Gemini-Flash", "Generating Investment Memo...")
#     AgentLogger.log("A2A-Protocol", "CRITIC ALERT: Claim unverified.")