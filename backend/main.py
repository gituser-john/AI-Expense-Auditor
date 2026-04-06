import os
import traceback
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
import models
from ai_engine import extract_raw_text, extract_policy_text, evaluate_expense

app = FastAPI(
    title="Expense Auditor API",
    description="Backend for the Policy-First Expense Auditor",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    # Create tables automatically on startup for development with SQLite
    models.Base.metadata.create_all(bind=engine)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/v1/receipts/upload")
async def upload_receipt(
    file: UploadFile = File(...),
    description: str = Form(...),
    user_id: int = Form(...), 
    db: Session = Depends(get_db)
):
    """
    Route for employees to upload a receipt + text description.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
            
        # Placeholder for background processes:
        # 1. Trigger OCR Service -> Extracts text
        # 2. Trigger AI Policy Engine -> Audits text against DB policies -> Generate verdict
        
        # Save preliminary receipt record
        new_receipt = models.Receipt(
            user_id=user_id,
            upload_path=file_path,
            description=description,
            verdict=models.VerdictEnum.pending
        )
        db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)
        
        return {
            "message": "Receipt uploaded successfully",
            "data": {
                "receipt_id": new_receipt.id,
                "upload_path": new_receipt.upload_path,
                "status": new_receipt.verdict.name
            }
        }
    except Exception as e:
        db.rollback()
        print(f"DB Error in /api/v1/receipts/upload: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/admin/claims")
async def fetch_all_claims(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Route for admins to fetch all processed claims.
    """
    receipts = db.query(models.Receipt).offset(skip).limit(limit).all()
    
    return {
        "message": "Claims fetched successfully",
        "skip": skip,
        "limit": limit,
        "data": receipts
    }


@app.post("/api/upload")
async def process_receipt(
    file: UploadFile = File(...),
    business_purpose: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Route for uploading a receipt and evaluating it against a local policy.pdf.
    """
    try:
        # 1. Temporarily save the uploaded receipt
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
            
        # 2. Parse Policy document
        policy_path = "policy.txt"
        policy_text = ""
        if os.path.exists(policy_path):
            with open(policy_path, 'r', encoding='utf-8') as f:
                policy_text = f.read()
            
        # 3. Extract RAW text from the receipt
        raw_receipt_text = extract_raw_text(file_path)
        
        # 4. Ask Gemini to evaluate the expense
        evaluation = evaluate_expense(raw_receipt_text, policy_text)
        
        # Add print statements right after OCR extraction and AI evaluation
        print("--- RAW OCR DATA ---")
        print(raw_receipt_text)
        print("--- AI EVALUATION (GEMINI JSON) ---")
        print(evaluation)
        print("--- END DEBUG MSG ---")

        # 5. Save the evaluation result to the database
        user = db.query(models.User).filter(models.User.id == 1).first()
        if not user:
            user = models.User(id=1, username="testuser", email="test@example.com")
            db.add(user)
            db.commit()

        # Safely map to VerdictEnum
        status_str = evaluation.get("status", "pending").lower()
        if status_str not in [e.value for e in models.VerdictEnum]:
            status_str = "pending"
            
        # Extract fields robustly
        merchant = evaluation.get("merchant_name", "")
        date_str = evaluation.get("date", "")
        try:
            total_amount = float(evaluation.get("total_amount", 0.0))
        except (ValueError, TypeError):
            total_amount = 0.0

        new_receipt = models.Receipt(
            user_id=1,
            upload_path=file_path,
            description="Uploaded via Dashboard",
            extracted_text=raw_receipt_text,
            merchant=merchant,
            date=date_str,
            business_purpose=business_purpose,
            total_amount=total_amount,
            verdict=models.VerdictEnum(status_str),
            verdict_reasoning=evaluation.get("citation", "No citation provided")
        )
        db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)
        
        # 6. Return structured JSON response including the DB id
        return {
            "id": new_receipt.id,
            "status": new_receipt.verdict.name,
            "citation": new_receipt.verdict_reasoning,
            "extracted_data": evaluation,
            "business_purpose": new_receipt.business_purpose
        }
    except Exception as e:
        db.rollback()
        print(f"DB Error in /api/upload: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/expenses")
async def get_expenses(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Route for the React Admin Dashboard to fetch all processed expenses.
    Returns them as a JSON array.
    """
    try:
        receipts = db.query(models.Receipt).offset(skip).limit(limit).all()
        # Convert SQLAlchemy objects to dicts so FastAPI can serialize them easily
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "upload_path": r.upload_path,
                "description": r.description,
                "merchant": r.merchant,
                "date": r.date,
                "business_purpose": r.business_purpose,
                "amount": float(r.total_amount) if r.total_amount is not None else None,
                "citation": r.verdict_reasoning,
                "ai_verdict": r.verdict.name if r.verdict else "pending",
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in receipts
        ]
    except Exception as e:
        print(f"DB Error in /api/expenses: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Make sure to run this using `python main.py` or `uvicorn main:app --reload`
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
