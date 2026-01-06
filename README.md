# 🤖 The Self-Correcting Investment Analyst

**A "Trust-First" Agentic RAG system for Financial Due Diligence.**

Most AI summarizers prioritize speed, often "hallucinating" numbers that look real but don't exist. This project builds a **compliance-grade engine** that uses a multi-agent "Critic Loop" to verify every claim against the source PDF before a human ever sees it.

---

## 🧠 The Architecture: "Maker-Checker" Loop

Unlike standard chatbots that work in a straight line (Input → Output), this system uses a **Finite State Machine (FSM)** to enforce a strict audit loop:

1. **The Analyst (Gemini Flash):** Reads the PDF and drafts a structured Investment Memo (Strengths, Risks, Verdict).
2. **The Critic (Gemini Pro/Flash):** Acts as a ruthlessly logical auditor. It cross-references every specific claim in the draft against the raw text chunks of the PDF.
   * *If a number doesn't match:* The draft is **REJECTED**. The Analyst is forced to retry.
   * *If hallucinations persist:* The system errors out for safety.
   * *If verified:* The draft is **APPROVED** and shown to the user.

---

## 🚀 Key Features

* **🛡️ Hallucination Guardrails:** The system auto-rejects unverified claims (e.g., "Revenue $10M" when the text says "$10M Projected").
* **📊 Structured Data Output:** Uses Pydantic to enforce strict JSON schemas for the memos (no random text blobs).
* **⚡ Split-Brain Processing:** Separates "Drafting" (Creativity/Speed) from "Auditing" (Logic/Compliance).
* **🖥️ Live "Hacker" Terminal:** Features a color-coded CLI that shows real-time state transitions, agent handshakes, and audit rejections.
* **📂 PDF Ingestion:** Custom parsing utility to handle messy pitch deck formatting.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/investment-analyst-mvp.git
cd investment-analyst-mvp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the Application

```bash
streamlit run main.py
```

---

## 🕹️ How to Use

1. **Upload a Pitch Deck:** Drag and drop a PDF file (e.g., Airbnb Series A deck) into the sidebar.
2. **Watch the Loop:**
   * Observe the terminal logs to see the agents talking (`[A2A-Protocol]`).
   * Watch the "State Machine" on the right side of the dashboard.

3. **Review the Output:**
   * If the **Critic** finds a hallucination, you will see a `REJECTED` status and the system will automatically loop back to `DRAFTING`.
   * Once the **Critic** is satisfied, the final verified Investment Memo appears.

---

## 🆚 Why is this better than a Chatbot?

| Feature | 🤖 Standard Chatbot | 🧠 Self-Correcting Analyst |
| --- | --- | --- |
| **Workflow** | Linear (Read → Write) | **Circular** (Draft → Audit → Fix → Finalize) |
| **Trust Model** | "Trust me, I'm smart." | **"Prove it."** (Zero Trust Architecture) |
| **Failure Mode** | Silent Failure (Confidently lies about numbers) | **Loud Rejection** (Stops process if facts can't be verified) |
| **Role** | Summarizer | **Compliance Officer** |

---

## 📁 File Structure

```plaintext
investment-analyst-mvp/
├── agents/             # The "Brains" (Analyst & Critic logic)
├── core/               # The "Rails" (Finite State Machine & Schemas)
├── protocols/          # The "Connectors" (MCP Server & Prompt Templates)
├── utils/              # Helpers (PDF Parser & Color Logger)
├── main.py             # Streamlit Dashboard Entry Point
└── config.py           # Model Configuration (Gemini 1.5 Flash)
```

---

## 📜 License

This project is open-source and available under the MIT License.

---

*Built with Google Gemini & Streamlit.*
