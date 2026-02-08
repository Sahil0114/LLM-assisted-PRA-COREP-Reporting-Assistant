"""
LLM Client - OpenAI integration for COREP field extraction
"""
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
import json

from config import Settings
from rag.vector_store import RetrievedDocument
from llm.structured_output import COREPFieldOutput, FieldMapping
from llm.prompts import get_extraction_prompt


class LLMClient:
    """OpenAI LLM client for regulatory field extraction."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def extract_corep_fields(
        self,
        question: str,
        scenario: Optional[str],
        context: List[RetrievedDocument],
        template_type: str
    ) -> COREPFieldOutput:
        """
        Extract COREP field values from the query and context.
        
        Returns structured output mapping values to template fields.
        """
        # Build context string from retrieved documents
        context_text = "\n\n---\n\n".join([
            f"**Source: {doc.reference}**\n{doc.content}"
            for doc in context
        ])
        
        # Get prompt
        system_prompt, user_prompt = get_extraction_prompt(
            template_type=template_type,
            question=question,
            scenario=scenario,
            context=context_text
        )
        
        # Call LLM with JSON mode
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,  # Low temperature for consistency
            max_tokens=2000
        )
        
        # Parse response
        response_text = response.choices[0].message.content
        response_data = json.loads(response_text)
        
        # Convert to structured output
        fields = []
        for field_data in response_data.get("fields", []):
            fields.append(FieldMapping(
                row=field_data.get("row"),
                column=field_data.get("column", "010"),
                field_name=field_data.get("field_name"),
                value=field_data.get("value"),
                currency=field_data.get("currency", "GBP"),
                source_reference=field_data.get("source_reference"),
                reasoning=field_data.get("reasoning")
            ))
        
        return COREPFieldOutput(
            template_type=template_type,
            fields=fields,
            reasoning=response_data.get("overall_reasoning", ""),
            confidence=response_data.get("confidence", 0.8),
            warnings=response_data.get("warnings", [])
        )
    
    async def validate_interpretation(
        self,
        field: FieldMapping,
        context: List[RetrievedDocument]
    ) -> Dict[str, Any]:
        """Validate an interpretation against regulatory text."""
        context_text = "\n\n".join([doc.content for doc in context])
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a regulatory compliance expert validating COREP field interpretations.
                    
Evaluate whether the proposed field value is consistent with the regulatory text provided.
Return a JSON object with:
- "is_valid": boolean
- "confidence": number 0-1
- "issues": list of any concerns
- "suggestions": list of any corrections"""
                },
                {
                    "role": "user",
                    "content": f"""Validate this field interpretation:

Field: {field.field_name} (Row {field.row})
Proposed Value: {field.value}
Reasoning: {field.reasoning}

Regulatory Context:
{context_text}"""
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        return json.loads(response.choices[0].message.content)
