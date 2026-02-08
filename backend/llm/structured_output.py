"""
Structured Output Schemas for LLM Responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class FieldMapping(BaseModel):
    """A single COREP field mapping."""
    row: str = Field(..., description="COREP template row number (e.g., '010')")
    column: str = Field(default="010", description="Column number, typically '010' for amount")
    field_name: str = Field(..., description="Human-readable field name")
    value: Optional[float] = Field(None, description="Numeric value for the field")
    currency: str = Field(default="GBP", description="Currency code")
    source_reference: Optional[str] = Field(None, description="Regulatory reference (e.g., 'CRR Article 26')")
    reasoning: Optional[str] = Field(None, description="Explanation for this value")


class COREPFieldOutput(BaseModel):
    """Complete structured output from LLM extraction."""
    template_type: str = Field(..., description="COREP template type (e.g., 'C01')")
    fields: List[FieldMapping] = Field(default_factory=list, description="Extracted field mappings")
    reasoning: str = Field(default="", description="Overall analysis reasoning")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    warnings: List[str] = Field(default_factory=list, description="Data quality or interpretation warnings")


class QueryResponse(BaseModel):
    """Response structure for API queries."""
    success: bool
    template_type: str
    fields: List[FieldMapping]
    validation_errors: List[str] = Field(default_factory=list)
    validation_warnings: List[str] = Field(default_factory=list)
    audit_trail: List[dict] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
