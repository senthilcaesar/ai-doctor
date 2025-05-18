import fitz  # PyMuPDF
import streamlit as st
import time
import io

def process_pdf(uploaded_file):
    """
    Process a PDF file using PyMuPDF to extract text.
    
    Args:
        uploaded_file: The uploaded PDF file from Streamlit
        
    Returns:
        dict: Contains extracted text and metadata
    """
    try:
        # Save the uploaded file to a temporary file
        with st.spinner("Processing PDF..."):
            # Read the file as bytes
            file_bytes = uploaded_file.read()
            
            # Open the PDF with PyMuPDF
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                # Get basic metadata
                metadata = {
                    "filename": uploaded_file.name,
                    "page_count": len(doc)
                }
                
                # Extract text with page numbers for reference
                full_text = ""
                for i, page in enumerate(doc):
                    text = page.get_text()
                    full_text += f"\n--- Page {i+1} ---\n{text}\n"
            
                return {
                    "success": True,
                    "metadata": metadata,
                    "text": full_text
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "metadata": {"filename": uploaded_file.name if hasattr(uploaded_file, 'name') else "unknown"},
            "text": ""
        }