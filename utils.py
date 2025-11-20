from PyPDF2 import PdfReader
import re

# Add your regex patterns for sensitive data here
PATTERNS = {
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "Passport": r"\b[A-Z]{1}[0-9]{7}\b|\b[K][0-9]{8}\b",
    "Medical Record": r"\b(MRN\d{6})\b",
    "Medical Test Results": r"\b(Result|Positive|Negative|Detected|Not Detected)\b",
    "Health Insurance": r"\bHIN\d{5}\b",
    "Credit Card": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
    "Aadhaar": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "Diagnosis": r"\b(Dementia|Stroke|Hypertension|Hyperlipidemia|Cardiac Failure|Renal Disease)\b",
}


def extract_text(file_path):
    """
    Extract text from a PDF file using PyPDF2.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


def scan_data(text):
    """
    Scan text for sensitive data based on regex patterns.
    """
    results = []
    for label, pattern in PATTERNS.items():
        matches = re.findall(pattern, text)
        for match in matches:
            results.append(
                {"type": label, "value": match, "classification": classify_data(label)}
            )
    return results


def classify_data(label):
    """
    Classify the type of data based on its label.
    """
    if label in ["PAN", "SSN", "Passport", "Aadhaar"]:
        return "PII"  # Personally Identifiable Information
    elif label in ["Medical Record", "Medical Test Results", "Diagnosis"]:
        return "PHI"  # Protected Health Information
    elif label in ["Credit Card"]:
        return "PCI"  # Payment Card Information
    elif label in ["Email"]:
        return "Contact Information"
    elif label in ["Health Insurance"]:
        return "Insurance Information"
    return "Unknown"
