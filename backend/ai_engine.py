import easyocr
import fitz  # PyMuPDF
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if API_KEY and API_KEY != "your_google_gemini_api_key_here":
    genai.configure(api_key=API_KEY)

_reader = None

def get_reader():
    """Lazily initializes the easyocr Reader."""
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader

def extract_raw_text(image_path: str) -> str:
    """
    Extracts raw text blob from an uploaded receipt image path using easyocr.
    """
    reader = get_reader()
    extracted_text_list = reader.readtext(image_path, detail=0)
    full_text = " ".join(extracted_text_list)
    return full_text

def extract_policy_text(pdf_path: str) -> str:
    """
    Parses and extracts text from a Travel Policy PDF using PyMuPDF (fitz).
    """
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def evaluate_expense(raw_receipt_text: str, policy_text: str) -> dict:
    """
    Evaluates the receipt text against the policy text using Gemini.
    Returns a strict JSON format matching the schema required by the DB.
    """
    if not API_KEY or API_KEY == "your_google_gemini_api_key_here":
        return {
            "merchant_name": "API Key Missing",
            "date": "YYYY-MM-DD",
            "total_amount": 0.0,
            "status": "pending",
            "citation": "Please configure GEMINI_API_KEY in .env file to run AI evaluation."
        }

    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = f"""
    You are an expert expense auditor assessing a receipt against a corporate travel policy.
    
    RECEIPT RAW TEXT:
    {raw_receipt_text}
    
    CORPORATE POLICY:
    {policy_text}
    
    Extract the merchant name, date, and total amount from the receipt.
    Format the date strictly as YYYY-MM-DD.
    Then, evaluate the expense against the policy and return a status and citation.
    Status MUST be exactly one of: "approved", "rejected", "flagged", or "pending".
    Provide a specific citation excerpt or reasoning based on the policy.

    Return EXACTLY a JSON object with this schema:
    {{
        "merchant_name": "string",
        "date": "string",
        "total_amount": number,
        "status": "string",
        "citation": "string"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print("Gemini API Error:", e)
        return {
            "merchant_name": "Gemini API Error",
            "date": "YYYY-MM-DD",
            "total_amount": 0.0,
            "status": "pending",
            "citation": str(e)
        }
