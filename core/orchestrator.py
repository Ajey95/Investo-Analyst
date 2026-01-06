# # core/orchestrator.py
# from core.state_schema import GlobalContext, WorkflowState, AuditResult, InvestmentMemo

# class Orchestrator:
#     def __init__(self):
#         self.context = GlobalContext()
#         self.MAX_RETRIES = 3

#     def get_context(self) -> GlobalContext:
#         """Returns the current state of the world."""
#         return self.context

#     def transition_to(self, new_state: WorkflowState):
#         """
#         Moves the FSM to a new state.
#         Includes Guardrails to prevent illegal transitions.
#         """
#         print(f"🔀 TRANSITION: {self.context.state.value} -> {new_state.value}")
#         self.context.state = new_state

#     def update_pdf_content(self, text: str):
#         """Action: Ingestion complete."""
#         self.context.raw_pdf_text = text
#         self.transition_to(WorkflowState.DRAFTING)

#     def update_draft(self, draft: InvestmentMemo):
#         """Action: Analyst finished drafting."""
#         self.context.current_draft = draft
#         self.transition_to(WorkflowState.CRITIQUING)

#     def process_audit(self, result: AuditResult):
#         """
#         Action: Critic finished auditing.
#         Logic: The Critic decides the next state (Loop vs Proceed).
#         """
#         self.context.audit_history.append(result)

#         if result.is_verified:
#             # Success: Move to Human Review
#             print("✅ Audit Passed. Sending to Human.")
#             self.transition_to(WorkflowState.AWAITING_HUMAN)
#         else:
#             # Failure: Check retry limits
#             if self.context.retry_count < self.MAX_RETRIES:
#                 print(f"❌ Audit Failed. Retrying ({self.context.retry_count + 1}/{self.MAX_RETRIES})...")
#                 self.context.retry_count += 1
#                 self.transition_to(WorkflowState.DRAFTING) # LOOP BACK
#             else:
#                 print("🛑 Max retries reached. Forcing Human Intervention.")
#                 self.transition_to(WorkflowState.ERROR)

#     def approve_final(self):
#         """Action: Human clicked 'Approve'."""
#         if self.context.current_draft:
#             # In a real app, this might generate a PDF or Email
#             self.context.final_report = self.context.current_draft.model_dump_json(indent=2)
#             self.transition_to(WorkflowState.FINALIZED)
# core/orchestrator.py
from core.state_schema import GlobalContext, WorkflowState, AuditResult, InvestmentMemo
from utils.logger import AgentLogger

class Orchestrator:
    def __init__(self):
        self.context = GlobalContext()
        self.MAX_RETRIES = 3

    def transition_to(self, new_state: WorkflowState):
        prev_state = self.context.state.value
        self.context.state = new_state
        
        if new_state == WorkflowState.AWAITING_HUMAN:
            AgentLogger.log("System", f"TRANSITION: {new_state.value}")
        else:
            AgentLogger.log("ADK-Orchestrator", f"State Transition: {prev_state} -> {new_state.value}")

    def update_pdf_content(self, text: str):
        self.context.raw_pdf_text = text
        self.transition_to(WorkflowState.DRAFTING)

    def update_draft(self, draft: InvestmentMemo):
        self.context.current_draft = draft
        self.transition_to(WorkflowState.CRITIQUING)

    def process_audit(self, result: AuditResult):
        self.context.audit_history.append(result)

        if result.is_verified:
            # SUCCESS LOGS
            AgentLogger.log("A2A-Protocol", f"APPROVED. Confidence: {result.score}/10")
            self.transition_to(WorkflowState.AWAITING_HUMAN)
        else:
            # FAILURE LOGS
            # Log the specific feedback items from the protocol
            AgentLogger.log("A2A-Protocol", f"CRITIC ALERT: {result.feedback[:50]}...") 
            AgentLogger.log("A2A-Protocol", "REJECTED. Sending feedback loop...")
            
            if self.context.retry_count < self.MAX_RETRIES:
                self.context.retry_count += 1
                AgentLogger.log("ADK-Orchestrator", f"Transition: CRITIQUING -> DRAFTING (Retry {self.context.retry_count}/{self.MAX_RETRIES})")
                self.context.state = WorkflowState.DRAFTING # Manual set to avoid double print, or use transition_to
            else:
                AgentLogger.log("ADK-Orchestrator", "Max retries reached. Stopping.")
                self.transition_to(WorkflowState.ERROR)

    def approve_final(self):
        if self.context.current_draft:
            self.context.final_report = self.context.current_draft.model_dump_json(indent=2)
            self.transition_to(WorkflowState.FINALIZED)