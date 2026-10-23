# 🚚 AI Logistics Copilot

An enterprise-grade, multi-agent AI logistics assistant powered by **Google Gemini 2.5**, **PostgreSQL + pgvector**, **Model Context Protocol (MCP)**, **Hybrid RAG**, and **Human-in-the-Loop (HITL)** guardrails.

Built as a flagship AI engineering portfolio project demonstrating production-oriented backend design, domain-driven modularity, and real-time streaming interfaces.

---

## 🌟 Key Architecture & Capabilities

```text
React 18 (Tailwind CSS, Glassmorphic UI, SSE Streaming)
       │
       ▼
FastAPI Backend (Feature-sliced: chat, shipments, approval, rag, eval)
       │
       ▼
AI Orchestrator (Google Gemini 2.5 SDK)
 ┌─────┴───────────────────────┬────────────────────────┐
 ▼                             ▼                        ▼
pgvector Hybrid RAG     Carrier Tools / MCP      PostgreSQL Memory & State
(Knowledge Retrieval)   (FedEx, UPS, DHL Mock)   (Active Shipment Drafts)
```

- **Domain-Driven Modular Backend**: Structured feature domains (`chat/`, `shipments/`, `approval/`, `rag/`, `eval/`) with strict separation of concerns (`models.py`, `services.py`, `cruds.py`, `routers.py`, `schemas.py`).
- **PostgreSQL 16 + pgvector**: Unified storage for relational session state and 768-dimensional vector embeddings with HNSW cosine similarity search.
- **Real-Time Streaming**: Server-Sent Events (SSE) streaming tokens directly from the Gemini 2.5 SDK to the React frontend.
- **Glassmorphic Dark UI**: Modern React + TypeScript interface styled with Tailwind CSS v3, responsive sidebars, and active workflow state inspection.

---

## 📁 Repository Structure

```text
ai-logistics-copilot/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entrypoint & lifespan
│   │   ├── config.py                # Environment & settings configuration
│   │   ├── core/
│   │   │   └── database.py          # Async SQLAlchemy engine & session factory
│   │   └── api/v1/
│   │       ├── chat/                # SSE streaming chat & session history
│   │       ├── shipments/           # Shipment draft workflows & Pydantic validation
│   │       ├── approval/            # Human-in-the-Loop booking authorization
│   │       ├── rag/                 # pgvector knowledge search & document ingestion
│   │       └── eval/                # Automated evaluation benchmarks & metrics
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Configuration template
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # Main streaming chat application
│   │   ├── index.css                # Tailwind directives & design system utilities
│   │   └── main.tsx                 # React entrypoint
│   ├── tailwind.config.js           # Custom glassmorphic color themes & glows
│   ├── vite.config.ts               # Vite proxy & build configuration
│   └── package.json                 # Node dependencies
├── docker-compose.yml               # PostgreSQL 16 + pgvector container
├── setup_and_testing_guide.md       # Step-by-step launch & verification guide
└── README.md
```

---

## 🚀 Quickstart

### 1. Database (Docker)
Ensure Docker Desktop is open, then start PostgreSQL with `pgvector`:
```bash
docker compose up -d
```

### 2. Backend (FastAPI)
```bash
# Configure environment
cp backend/.env.example backend/.env
# (Add your GEMINI_API_KEY inside backend/.env)

# Install dependencies & run server
pip install -r backend/requirements.txt
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`

### 3. Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:3000`

---

## 🗺️ Roadmap & Implementation Phases

- [x] **V1: Core AI Chat & Infrastructure** — Feature-sliced FastAPI backend, PostgreSQL + pgvector, React Tailwind chat UI, and Gemini SSE streaming.
- [ ] **V2: Structured Output Layer** — Natural language shipment extraction to validated Pydantic schemas & UI `ShipmentCard`.
- [ ] **V3: Tool Calling Layer** — Mock FedEx, UPS, and DHL carrier rating & tracking integrations.
- [ ] **V4: RAG Engine with pgvector** — Hybrid search across carrier guides and customs regulations.
- [ ] **V5: Memory & Workflow State** — Multi-turn active shipment draft persistence.
- [ ] **V6: Autonomous Multi-Step Agent** — Multi-carrier comparison and recommendation planner.
- [ ] **V7: Model Context Protocol (MCP)** — Custom `logistics-mcp-server` integration.
- [ ] **V8: Evaluation Framework** — 100-scenario benchmark suite & metrics dashboard.
- [ ] **V9: Guardrails & Human-in-the-Loop** — High-impact booking approval modal & safety filters.
