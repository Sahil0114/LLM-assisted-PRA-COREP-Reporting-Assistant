"""
Audit Logger - Track regulatory citations for each field
"""
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass

from llm.structured_output import FieldMapping
from rag.vector_store import RetrievedDocument


@dataclass
class AuditEntry:
    """A single audit trail entry."""
    field_row: str
    field_name: str
    value: Any
    source_reference: str
    source_content: str
    reasoning: str
    timestamp: str


class AuditLogger:
    """
    Audit logger for COREP field population.
    
    Tracks which regulatory paragraphs were used to justify each populated field,
    providing full traceability for compliance purposes.
    """
    
    def __init__(self):
        self.entries: List[AuditEntry] = []
    
    def create_trail(
        self,
        fields: List[FieldMapping],
        sources: List[RetrievedDocument],
        reasoning: str
    ) -> List[Dict[str, Any]]:
        """
        Create an audit trail linking fields to their regulatory sources.
        
        Args:
            fields: Extracted field mappings from LLM
            sources: Retrieved regulatory documents
            reasoning: Overall reasoning from LLM
            
        Returns:
            List of audit entries as dictionaries
        """
        audit_trail = []
        timestamp = datetime.now().isoformat()
        
        # Create a lookup for sources by reference
        source_lookup = {
            doc.reference: doc for doc in sources
        }
        
        for field in fields:
            # Find the matching source document
            source_doc = None
            source_content = ""
            
            if field.source_reference:
                # Try exact match first
                source_doc = source_lookup.get(field.source_reference)
                
                # Try partial match if no exact match
                if not source_doc:
                    for ref, doc in source_lookup.items():
                        if field.source_reference in ref or ref in field.source_reference:
                            source_doc = doc
                            break
                
                if source_doc:
                    source_content = source_doc.content[:500]  # Truncate for display
            
            entry = {
                "field_row": field.row,
                "field_name": field.field_name,
                "value": field.value,
                "currency": field.currency,
                "source_reference": field.source_reference or "Not specified",
                "source_content": source_content or "Source text not available",
                "reasoning": field.reasoning or "No specific reasoning provided",
                "timestamp": timestamp,
                "confidence_indicators": self._assess_confidence(field, source_doc)
            }
            
            audit_trail.append(entry)
            self.entries.append(AuditEntry(**{
                k: v for k, v in entry.items() 
                if k != "confidence_indicators"
            }))
        
        # Add overall analysis entry
        audit_trail.append({
            "field_row": "OVERALL",
            "field_name": "Analysis Summary",
            "value": None,
            "source_reference": f"Based on {len(sources)} regulatory sources",
            "source_content": reasoning,
            "reasoning": reasoning,
            "timestamp": timestamp,
            "confidence_indicators": {
                "sources_used": len(sources),
                "fields_populated": len(fields)
            }
        })
        
        return audit_trail
    
    def _assess_confidence(
        self,
        field: FieldMapping,
        source_doc: RetrievedDocument | None
    ) -> Dict[str, Any]:
        """Assess confidence indicators for an audit entry."""
        indicators = {
            "has_source_reference": bool(field.source_reference),
            "has_reasoning": bool(field.reasoning),
            "source_retrieved": bool(source_doc),
            "source_relevance": "N/A"
        }
        
        if source_doc:
            indicators["source_relevance"] = (
                "High" if source_doc.score > 0.8
                else "Medium" if source_doc.score > 0.6
                else "Low"
            )
        
        return indicators
    
    def export_trail(self, format: str = "json") -> str:
        """Export the audit trail in specified format."""
        import json
        
        if format == "json":
            return json.dumps([
                {
                    "field_row": e.field_row,
                    "field_name": e.field_name,
                    "value": e.value,
                    "source_reference": e.source_reference,
                    "reasoning": e.reasoning,
                    "timestamp": e.timestamp
                }
                for e in self.entries
            ], indent=2)
        
        # Could add CSV, PDF export etc.
        raise ValueError(f"Unsupported export format: {format}")
