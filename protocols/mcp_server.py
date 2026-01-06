# protocols/mcp_server.py
from typing import Dict
from utils.pdf_parser import parse_pdf_from_stream

class LocalMCPServer:
    """
    Simulates a Model Context Protocol (MCP) server.
    Responsible for ingesting 'Resources' (PDFs) and serving 'Context' (Text chunks).
    """
    
    def __init__(self):
        self.document_cache: Dict[str, str] = {} 

    def ingest_pdf(self, file_stream) -> str:
        """
        Delegates parsing to the utility function.
        """
        # Call the helper function from utils/pdf_parser.py
        full_text = parse_pdf_from_stream(file_stream)
        
        if full_text:
            self.document_cache["current_doc"] = full_text
            print(f"✅ PDF Ingested: {len(full_text)} chars extracted.")
        else:
            print("❌ Failed to extract text from PDF.")

        return full_text

    def get_context(self) -> str:
        """
        Retrieves the currently loaded document context.
        """
        return self.document_cache.get("current_doc", "")

# Singleton instance
mcp = LocalMCPServer()