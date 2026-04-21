import sys
import subprocess
import os

def read_pdf_cli(file_path):
    """Fallback: Try using pdftotext CLI tool."""
    try:
        result = subprocess.run(['pdftotext', file_path, '-'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return None
    except FileNotFoundError:
        return None

def read_pdf_pypdf(file_path):
    """Primary: Try using pypdf library."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text if text.strip() else None
    except ImportError:
        return None
    except Exception as e:
        return f"Error using pypdf: {str(e)}"

def read_pdf(file_path):
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    # Strategy 1: Try pypdf (more robust if installed)
    content = read_pdf_pypdf(file_path)
    if content and not content.startswith("Error"):
        return content
    
    # Strategy 2: Try pdftotext CLI (fallback)
    content_cli = read_pdf_cli(file_path)
    if content_cli:
        return content_cli
        
    # If both fail
    error_msg = "Error: Failed to extract text from PDF.\n"
    error_msg += "- pypdf: Not installed or failed to extract text.\n"
    error_msg += "- pdftotext: Not found in system PATH.\n"
    error_msg += "Please install one of them: 'pip install pypdf' or 'brew install poppler'."
    return error_msg

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read-pdf.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = os.path.expanduser(sys.argv[1])
    print(read_pdf(pdf_path))
