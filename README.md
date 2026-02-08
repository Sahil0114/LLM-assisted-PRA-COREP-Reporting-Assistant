COREP Reporting Assistant

LLM-assisted regulatory reporting prototype for PRA COREP submissions.

Quick Start

Backend
```bash
cd backend
pip install -r requirements.txt
# Set your OpenAI API key
set OPENAI_API_KEY=your_key_here
uvicorn main:app --reload --port 8000
```

Frontend  
```bash
cd frontend
npm install
npm run dev
```
Features
- Natural language queries for COREP template population
- RAG-based retrieval of PRA Rulebook and COREP instructions
- C01 Own Funds template with validation rules
- Audit trail linking fields to regulatory paragraphs
