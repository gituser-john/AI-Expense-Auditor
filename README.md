# Corporate AI Expense Auditor

## The Problem
Manual auditing of corporate travel and expense receipts is a tedious, error-prone, and inefficient process. Finance teams waste countless hours visually inspecting physical receipts and cross-referencing them against complex corporate policies to detect overspending or restricted purchases (such as alcohol).

## The Solution
This project automates the receipt auditing process by combining Optical Character Recognition (OCR) with Large Language Models (LLMs). The approach uses a React frontend for employees to upload physical receipt images, which are sent to a FastAPI backend. EasyOCR extracts the raw text and financial data from the image, and the Google Gemini API acts as an AI auditor, evaluating the parsed data against a plain-text corporate policy document. 

**Key Features:**
*   **Computer Vision Ingestion:** Automatically extracts text, line items, and totals from receipt images of varying quality.
*   **AI Policy Enforcement:** Dynamically reads corporate rules and issues definitive "Approved" or "Rejected" verdicts.
*   **Automated Citation:** Cites the exact section of the corporate policy that caused an expense to be flagged.
*   **Dual Dashboards:** Includes an employee upload portal and an admin dashboard to view the database of audited expenses.

## Tech Stack
*   **Programming Languages:** Python 3, JavaScript (ES6+), HTML/CSS
*   **Frameworks:** React.js (Vite), FastAPI, Uvicorn
*   **Databases:** SQLite (managed via SQLAlchemy ORM)
*   **APIs or third-party tools:** 
    *   Google Gemini API (`gemini-2.5-flash`) for logical evaluation
    *   EasyOCR & PyTorch for text extraction
    *   Axios / Fetch API for client-server communication

## Setup Instructions

### Prerequisites
*   Node.js installed (v16+)
*   Python installed (v3.10+)
*   A Google Gemini API Key

### 1. Backend Setup
Open a terminal, navigate to the project root, and follow these steps:

```bash

# Create and activate a virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# In another terminal
.venv\Scripts\activate

# Navigate into the frontend folder
cd frontend

# Install all required Node modules
npm install

# Start the Vite development server
npm run dev