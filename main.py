# main.py
import streamlit as st
import asyncio
from core.orchestrator import Orchestrator
from core.state_schema import WorkflowState
from protocols.mcp_server import mcp
from agents.analyst_agent import AnalystAgent
from agents.critic_agent import CriticAgent

# --- PAGE CONFIG ---
st.set_page_config(page_title="Self-Correcting Analyst", layout="wide")

# --- INITIALIZATION ---
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()
    st.session_state.analyst = AnalystAgent()
    st.session_state.critic = CriticAgent()

orc = st.session_state.orchestrator

# --- SIDEBAR ---
with st.sidebar:
    st.title("🤖 Investment Analyst")
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Pitch Deck (PDF)", type="pdf")
    
    if st.button("Reset System"):
        del st.session_state.orchestrator
        st.rerun()

# --- MAIN UI ---
st.title("Self-Correcting Investment Due Diligence")

# Create two columns: Context (Left) vs. Agent Loop (Right)
col1, col2 = st.columns([1, 1])

# === LEFT COLUMN: PDF CONTEXT ===
with col1:
    st.subheader("📄 Document Context")
    if uploaded_file:
        # Ingestion Step
        if orc.context.state == WorkflowState.INITIAL:
            with st.spinner("Ingesting PDF..."):
                text = mcp.ingest_pdf(uploaded_file)
                orc.update_pdf_content(text)
                st.success("PDF Ingested & Chunked.")
        
        # Display extracted text (Preview)
        st.text_area("Extracted Text", value=orc.context.raw_pdf_text, height=600)
    else:
        st.info("Please upload a PDF to begin.")

# === RIGHT COLUMN: AGENT WORKFLOW ===
with col2:
    st.subheader("⚙️ Agent State Machine")
    
    # State Display
    current_state = orc.context.state.value
    st.info(f"Current State: **{current_state}**")

    # 1. DRAFTING PHASE
    if orc.context.state == WorkflowState.DRAFTING:
        if st.button("▶ Start Analyst Agent"):
            with st.status("Analyst is working...", expanded=True) as status:
                st.write("Reading context...")
                draft = st.session_state.analyst.generate_draft(orc.context.raw_pdf_text)
                st.write("Draft generated!")
                orc.update_draft(draft)
                status.update(label="Drafting Complete", state="complete")
            st.rerun()

    # 2. CRITIQUING PHASE
    elif orc.context.state == WorkflowState.CRITIQUING:
        st.markdown("### 📝 Draft Generated")
        st.json(orc.context.current_draft.model_dump())
        
        if st.button("▶ Run Critic Audit"):
            with st.status("Critic is reviewing...", expanded=True) as status:
                st.write("Cross-referencing claims...")
                audit = st.session_state.critic.critique_draft(
                    orc.context.raw_pdf_text, 
                    orc.context.current_draft
                )
                orc.process_audit(audit)
                status.update(label="Audit Complete", state="complete")
            st.rerun()

    # 3. HUMAN REVIEW (SUCCESS)
    elif orc.context.state == WorkflowState.AWAITING_HUMAN:
        st.success("✅ Verification Passed! No hallucinations found.")
        
        st.markdown("### 🏆 Final Investment Memo")
        memo = orc.context.current_draft
        st.write(f"**Company:** {memo.company_name}")
        st.write(f"**Verdict:** {memo.verdict}")
        st.write(f"**Summary:** {memo.executive_summary}")
        
        st.markdown("**Key Strengths:**")
        for s in memo.key_strengths:
            st.write(f"- {s}")
            
        st.markdown("**Risks:**")
        for r in memo.risks:
            st.write(f"- {r}")

        if st.button("Approve & Finalize"):
            orc.approve_final()
            st.rerun()

    # 4. FINALIZED
    elif orc.context.state == WorkflowState.FINALIZED:
        st.balloons()
        st.title("🚀 Report Finalized")
        st.json(orc.context.final_report)

    # 5. ERROR / RETRY LOOP VISUALIZATION
    # Show audit history if any exist
    if orc.context.audit_history:
        with st.expander("Show Audit History (Critic Feedback)"):
            for i, audit in enumerate(orc.context.audit_history):
                st.write(f"**Attempt {i+1}:** Verified={audit.is_verified}")
                st.write(f"Feedback: {audit.feedback}")
                st.write("---")