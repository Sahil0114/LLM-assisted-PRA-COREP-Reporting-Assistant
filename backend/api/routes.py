"""
API Routes for COREP Reporting Assistant
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from config import get_settings, Settings
from llm.llm_client import LLMClient
from llm.structured_output import COREPFieldOutput, QueryResponse
from templates.c01_own_funds import C01OwnFundsTemplate, populate_template
from templates.validator import ValidationEngine
from audit.audit_logger import AuditLogger


router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for regulatory queries."""
    question: str = Field(..., description="Natural language question about COREP reporting")
    scenario: Optional[str] = Field(None, description="Description of the reporting scenario")
    template_type: str = Field(default="C01", description="COREP template type (e.g., C01)")


class TemplateResponse(BaseModel):
    """Response model with populated template."""
    template_type: str
    template_data: Dict[str, Any]
    validation_results: List[Dict[str, Any]]
    audit_trail: List[Dict[str, Any]]
    retrieved_sources: List[Dict[str, str]]
    timestamp: str


@router.post("/query", response_model=TemplateResponse)
async def process_query(
    request: QueryRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Process a natural language query and return a populated COREP template.
    
    Flow:
    1. Retrieve relevant regulatory text via RAG
    2. Send to LLM for structured field extraction
    3. Map to COREP template
    4. Validate against EBA rules
    5. Generate audit trail
    """
    try:
        # Initialize components
        llm_client = LLMClient(settings)
        validator = ValidationEngine()
        audit_logger = AuditLogger()
        
        # Step 1: Retrieve relevant regulatory text
        from main import vector_store
        retrieved_docs = await vector_store.retrieve(
            query=request.question,
            scenario=request.scenario,
            k=5
        )
        
        # Step 2: LLM processing for structured output
        llm_response = await llm_client.extract_corep_fields(
            question=request.question,
            scenario=request.scenario,
            context=retrieved_docs,
            template_type=request.template_type
        )
        
        # Step 3: Map to COREP template
        template = populate_template(
            template_type=request.template_type,
            field_data=llm_response.fields
        )
        
        # Step 4: Validate
        validation_results = validator.validate(
            template=template,
            template_type=request.template_type
        )
        
        # Step 5: Generate audit trail
        audit_trail = audit_logger.create_trail(
            fields=llm_response.fields,
            sources=retrieved_docs,
            reasoning=llm_response.reasoning
        )
        
        return TemplateResponse(
            template_type=request.template_type,
            template_data=template.model_dump(),
            validation_results=validation_results,
            audit_trail=audit_trail,
            retrieved_sources=[
                {"content": doc.content[:200] + "...", "reference": doc.reference}
                for doc in retrieved_docs
            ],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/{template_type}")
async def get_template_schema(template_type: str):
    """Get the schema for a COREP template type."""
    if template_type == "C01":
        return {
            "template_type": "C01",
            "name": "Own Funds",
            "description": "COREP Own Funds template for reporting capital components",
            "fields": C01OwnFundsTemplate.model_json_schema()
        }
    raise HTTPException(status_code=404, detail=f"Template {template_type} not found")


@router.get("/validation-rules/{template_type}")
async def get_validation_rules(template_type: str):
    """Get validation rules for a COREP template type."""
    validator = ValidationEngine()
    return validator.get_rules(template_type)
