# utils/pdf_parser.py
import pypdf
import re

def parse_pdf_from_stream(file_stream) -> str:
    """
    Extracts text from a PDF file stream (like from Streamlit).
    Performs basic cleaning to remove excessive whitespace.
    """
    try:
        reader = pypdf.PdfReader(file_stream)
        full_text = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Cleaning: Replace multiple spaces/newlines with a single space
                # This saves tokens and helps the LLM focus.
                cleaned_text = re.sub(r'\s+', ' ', text).strip()
                
                # We keep page numbers as anchors for the Critic Agent
                full_text.append(f"[PAGE {i+1}]: {cleaned_text}")

        return "\n\n".join(full_text)
        
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""