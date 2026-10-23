# AI Logistics Copilot — Setup & Testing Guide

This guide provides step-by-step instructions to set up, run, and verify the **AI Logistics Copilot** system across backend, frontend, and database services.

---

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: v20 or higher & npm
- **PostgreSQL**: 16+ with `pgvector` extension (Optional for basic API/Chat testing; required for full DB persistence & vector RAG)
- **Google Gemini API Key**: Obtain a key from [Google AI Studio](https://aistudio.google.com/)

---

## 🛠️ Step 1: Environment Setup

Navigate to the project root:

```bash
cd "d:/Artificial Inteligence/Implementation one"
```

### 1.1 Backend Environment Configuration
Create a `.env` file inside `backend/`:

```bash
# Windows PowerShell
Copy-Item backend\.env.example backend\.env
```

Edit `backend/.env` and insert your Gemini API Key:

```env
PROJECT_NAME="AI Logistics Copilot"
API_V1_STR="/api/v1"
GEMINI_API_KEY="AIzaSyYourActualGeminiApiKeyHere"
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/logistics_db"
LOG_LEVEL="INFO"
```

---

## 🚀 Step 2: Launch Backend FastAPI Server

### 2.1 Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r backend/requirements.txt
```

### 2.2 Start FastAPI Server

```bash
# Change directory to backend
cd backend

# Launch uvicorn dev server
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at:
- **API Base**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

---

## 💻 Step 3: Launch Frontend React App

In a **new terminal window**:

```bash
# Navigate to frontend folder
cd "d:/Artificial Inteligence/Implementation one/frontend"

# Install Tailwind & React dependencies
npm install

# Start Vite dev server
npm run dev
```

The frontend UI will be running at: `http://localhost:3000`

---

## 🧪 Step 4: Verification & Testing Commands

### 4.1 Health Check Test
```bash
curl http://localhost:8000/health
```
**Expected Response**:
```json
{
  "status": "healthy",
  "service": "AI Logistics Copilot",
  "version": "1.0.0"
}
```

### 4.2 Non-Streaming Chat API Test
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"content": "Compare FedEx and UPS rates from Chennai to Bangalore for 50kg."}'
```

### 4.3 RAG Ingestion & Query Test
```bash
# Ingest document
curl -X POST http://localhost:8000/api/v1/rag/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_title": "FedEx_Export_Policy_2026",
    "carrier": "FedEx",
    "content": "For international export shipments valued over $2500 USD, an EEI electronic filing is mandatory prior to departure."
  }'

# Query knowledge base
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "When is EEI filing mandatory?",
    "top_k": 3
  }'
```

### 4.4 Evaluation Benchmark Metrics Test
```bash
# Trigger benchmark run
curl -X POST http://localhost:8000/api/v1/eval/run \
  -H "Content-Type: application/json" \
  -d '{"num_samples": 5}'

# Fetch aggregate metrics summary
curl http://localhost:8000/api/v1/eval/metrics
```

### 4.5 Interactive Frontend Testing
1. Open `http://localhost:3000` in your web browser.
2. Observe the dark mode glassmorphic UI styled with Tailwind CSS.
3. Click the sample query button: **"🚚 Rate Comparison (Chennai ➔ Bangalore)"**.
4. Observe real-time streaming tokens delivered directly from Gemini 2.5 SDK.

---

## 🛠️ Summary of Modular Endpoint Routes

| Domain | Router File | Endpoint Base | Key Features |
| :--- | :--- | :--- | :--- |
| **Chat** | `app/api/v1/chat/routers.py` | `/api/v1/chat` | SSE streaming, session history, Gemini SDK |
| **Shipments** | `app/api/v1/shipments/routers.py` | `/api/v1/shipments` | Active workflow state & rate calculations |
| **Approval** | `app/api/v1/approval/routers.py` | `/api/v1/approval` | Human-in-the-loop booking confirmations |
| **RAG** | `app/api/v1/rag/routers.py` | `/api/v1/rag` | `pgvector` similarity search & chunking |
| **Eval** | `app/api/v1/eval/routers.py` | `/api/v1/eval` | Benchmark test suite & metrics dashboard |
