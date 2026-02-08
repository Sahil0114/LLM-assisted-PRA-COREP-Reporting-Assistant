"""
COREP Reporting Assistant - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import get_settings
from api.routes import router
from rag.vector_store import VectorStore


# Global vector store instance
vector_store: VectorStore = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - initialize resources on startup."""
    global vector_store
    settings = get_settings()
    
    # Initialize vector store
    vector_store = VectorStore(settings)
    await vector_store.initialize()
    
    yield
    
    # Cleanup on shutdown
    pass


app = FastAPI(
    title="COREP Reporting Assistant",
    description="LLM-assisted regulatory reporting for PRA COREP submissions",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "app": "COREP Reporting Assistant",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
