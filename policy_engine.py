import pytesseract
import fitz  # PyMuPDF
import re
import json
from PIL import Image
import os

def extract_receipt_data(image_path: str) -> dict:
    """
    Extracts the Merchant Name, Date, Total Amount, and Currency from an uploaded receipt image.
    Uses pytesseract for OCR and basic regex for field extraction as a prototype.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    try:
        # Load the image and run OCR
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        
        # --- Prototype Regex Extractions ---
        
        # 1. Date extraction (e.g., DD/MM/YYYY, YYYY-MM-DD)
        date_match = re.search(r'\b(\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4})\b', text)
        date = date_match.group(1) if date_match else "Unknown"
        
        # 2. Amount extraction (e.g., matching 123.45 with optional currency prefix)
        amount_match = re.search(r'[\$£€]?\s*(\d+\.\d{2})', text)
        amount = amount_match.group(1) if amount_match else "0.00"
        
        # 3. Currency extraction (heuristic based on common symbols or codes)
        currency_match = re.search(r'([\$£€]|USD|EUR|GBP)', text)
        currency = currency_match.group(1) if currency_match else "Unknown"
        
        # 4. Merchant Name (heuristic: generally the first non-empty line on a receipt)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        merchant_name = lines[0] if lines else "Unknown"
        
        return {
            "merchant_name": merchant_name,
            "date": date,
            "total_amount": amount,
            "currency": currency,
            "raw_text": text
        }
    except Exception as e:
        print(f"Error processing receipt image: {e}")
        return {
            "merchant_name": "Unknown",
            "date": "Unknown",
            "total_amount": "0.00",
            "currency": "Unknown",
            "raw_text": ""
        }

def parse_policy_pdf(pdf_path: str) -> str:
    """
    Parses text from a sample Travel Policy PDF using PyMuPDF (fitz).
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at path: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        text_chunks = []
        for page in doc:
            text_chunks.append(page.get_text())
        return "\n".join(text_chunks)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def evaluate_expense(receipt_data: dict, policy_text: str) -> str:
    """
    Mock AI evaluation function.
    Takes extracted receipt data, compares it against a chunk of policy text, and returns a JSON object.
    You can replace the logic inside with a call to an LLM API later.
    """
    amount = float(receipt_data.get("total_amount", 0.0))
    merchant = receipt_data.get("merchant_name", "").lower()
    policy_lower = policy_text.lower()
    
    # Defaults
    status = "Approved"
    citation = "The expense complies with standard policy guidelines."

    # --- Basic Mock Logic / Keyword Matching ---
    
    # Rule 1: Missing essential data
    if amount == 0.0 or merchant == "unknown":
        status = "Flagged"
        citation = "Unable to read key receipt details accurately; requires manual review."

    # Rule 2: Exceeding a hardcoded policy limit found via keyword mock
    elif "limit" in policy_lower and amount > 1000.0:
        status = "Rejected"
        citation = "Per the policy limits, single expenses cannot exceed standard threshold (1000)."
    
    # Rule 3: Flag items related to alcohol or bars if policy restricts 'alcohol'
    elif "alcohol" in policy_lower and ("bar" in merchant or "pub" in merchant or "liquor" in merchant):
         status = "Rejected"
         citation = "Policy explicitly prohibits reimbursement for alcohol or at bar/pub establishments."
         
    # Rule 4: General flag for high value
    elif amount > 500.0:
        status = "Flagged"
        citation = "Expenses over 500 require higher-level managerial review based on policy terms."
    
    result = {
        "status": status,
        "citation": citation,
        "receipt_evaluated": receipt_data.get("merchant_name", "Unknown"),
        "amount_evaluated": receipt_data.get("total_amount", "0.00")
    }
    
    return json.dumps(result, indent=4)

if __name__ == "__main__":
    # --- Quick Local Test Stub ---
    sample_receipt = {
        "merchant_name": "Downtown Pub & Drinks",
        "date": "2024-05-15",
        "total_amount": "120.00",
        "currency": "USD"
    }
    sample_policy = "Employees are not allowed to expense alcohol or personal entertainment. Meal limits are strictly observed."
    
    print("Evaluating sample receipt against mock policy:")
    print(evaluate_expense(sample_receipt, sample_policy))
