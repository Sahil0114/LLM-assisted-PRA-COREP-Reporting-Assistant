"""
C01 Own Funds Template - COREP Template Schema and Mapping
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from llm.structured_output import FieldMapping


class C01OwnFundsTemplate(BaseModel):
    """
    COREP C01 Own Funds Template
    
    This template captures the composition of regulatory own funds
    according to CRR (Capital Requirements Regulation).
    """
    
    # CET1 Capital Components
    row_010: Optional[float] = Field(None, description="Capital instruments eligible as CET1")
    row_020: Optional[float] = Field(None, description="Share premium related to CET1 instruments")
    row_030: Optional[float] = Field(None, description="Retained earnings")
    row_040: Optional[float] = Field(None, description="Accumulated other comprehensive income")
    row_050: Optional[float] = Field(None, description="Other reserves")
    row_060: Optional[float] = Field(None, description="Minority interests (amount allowed in consolidated CET1)")
    row_070: Optional[float] = Field(None, description="Independent interim/year-end profits")
    
    # CET1 Adjustments
    row_080: Optional[float] = Field(None, description="(-) Goodwill and other intangible assets")
    row_090: Optional[float] = Field(None, description="(-) Deferred tax assets depending on future profitability")
    row_095: Optional[float] = Field(None, description="(-) Shortfall of provisions to expected losses")
    
    # CET1 Totals
    row_100: Optional[float] = Field(None, description="CET1 capital before regulatory adjustments")
    row_200: Optional[float] = Field(None, description="CET1 capital after regulatory adjustments")
    
    # AT1 Components
    row_300: Optional[float] = Field(None, description="Additional Tier 1 (AT1) instruments")
    row_310: Optional[float] = Field(None, description="Share premium related to AT1 instruments")
    row_320: Optional[float] = Field(None, description="(-) AT1 deductions")
    
    # Tier 1 Total
    row_400: Optional[float] = Field(None, description="Tier 1 capital (CET1 + AT1)")
    
    # Tier 2 Components
    row_500: Optional[float] = Field(None, description="Tier 2 instruments")
    row_510: Optional[float] = Field(None, description="Share premium related to T2 instruments")
    row_520: Optional[float] = Field(None, description="(-) Tier 2 deductions")
    
    # Tier 2 Total
    row_600: Optional[float] = Field(None, description="Tier 2 capital")
    
    # Total Own Funds
    row_700: Optional[float] = Field(None, description="TOTAL OWN FUNDS")
    
    # Currency
    currency: str = Field(default="GBP", description="Reporting currency")
    
    class Config:
        json_schema_extra = {
            "example": {
                "row_010": 1000000000,
                "row_030": 200000000,
                "row_100": 1200000000,
                "row_200": 1150000000,
                "row_300": 50000000,
                "row_400": 1200000000,
                "row_500": 100000000,
                "row_600": 100000000,
                "row_700": 1300000000,
                "currency": "GBP"
            }
        }


# Field metadata for display and validation
FIELD_METADATA = {
    "row_010": {
        "label": "Capital instruments eligible as CET1",
        "crr_article": "Article 26(1)(a)",
        "category": "CET1",
        "is_total": False
    },
    "row_020": {
        "label": "Share premium related to CET1 instruments",
        "crr_article": "Article 26(1)(b)",
        "category": "CET1",
        "is_total": False
    },
    "row_030": {
        "label": "Retained earnings",
        "crr_article": "Article 26(1)(c)",
        "category": "CET1",
        "is_total": False
    },
    "row_040": {
        "label": "Accumulated other comprehensive income",
        "crr_article": "Article 26(1)(d)",
        "category": "CET1",
        "is_total": False
    },
    "row_050": {
        "label": "Other reserves",
        "crr_article": "Article 26(1)(e)",
        "category": "CET1",
        "is_total": False
    },
    "row_060": {
        "label": "Minority interests",
        "crr_article": "Article 84",
        "category": "CET1",
        "is_total": False
    },
    "row_100": {
        "label": "CET1 capital before adjustments",
        "crr_article": "Article 26",
        "category": "CET1",
        "is_total": True
    },
    "row_200": {
        "label": "CET1 capital",
        "crr_article": "Article 50",
        "category": "CET1",
        "is_total": True
    },
    "row_300": {
        "label": "AT1 instruments",
        "crr_article": "Article 51",
        "category": "AT1",
        "is_total": False
    },
    "row_400": {
        "label": "Tier 1 capital",
        "crr_article": "Article 25",
        "category": "Tier 1",
        "is_total": True
    },
    "row_500": {
        "label": "Tier 2 instruments",
        "crr_article": "Article 62",
        "category": "Tier 2",
        "is_total": False
    },
    "row_600": {
        "label": "Tier 2 capital",
        "crr_article": "Article 71",
        "category": "Tier 2",
        "is_total": True
    },
    "row_700": {
        "label": "TOTAL OWN FUNDS",
        "crr_article": "Article 72",
        "category": "Total",
        "is_total": True
    }
}


def populate_template(template_type: str, field_data: List[FieldMapping]) -> C01OwnFundsTemplate:
    """
    Populate a C01 template from extracted field mappings.
    """
    if template_type != "C01":
        raise ValueError(f"Unsupported template type: {template_type}")
    
    template_dict = {"currency": "GBP"}
    
    for field in field_data:
        row_key = f"row_{field.row.zfill(3)}"
        if hasattr(C01OwnFundsTemplate, row_key):
            template_dict[row_key] = field.value
        if field.currency:
            template_dict["currency"] = field.currency
    
    # Calculate derived totals if not provided
    template = C01OwnFundsTemplate(**template_dict)
    
    # Auto-calculate CET1 before adjustments if components are present
    if template.row_100 is None:
        components = [
            template.row_010 or 0,
            template.row_020 or 0,
            template.row_030 or 0,
            template.row_040 or 0,
            template.row_050 or 0,
            template.row_060 or 0,
            template.row_070 or 0
        ]
        if any(c > 0 for c in components):
            template.row_100 = sum(components)
    
    # Auto-calculate CET1 after adjustments
    if template.row_200 is None and template.row_100 is not None:
        deductions = sum([
            template.row_080 or 0,
            template.row_090 or 0,
            template.row_095 or 0
        ])
        template.row_200 = template.row_100 - abs(deductions)
    
    # Auto-calculate Tier 1
    if template.row_400 is None:
        cet1 = template.row_200 or 0
        at1 = (template.row_300 or 0) + (template.row_310 or 0) - abs(template.row_320 or 0)
        if cet1 > 0 or at1 > 0:
            template.row_400 = cet1 + at1
    
    # Auto-calculate Tier 2
    if template.row_600 is None:
        t2 = (template.row_500 or 0) + (template.row_510 or 0) - abs(template.row_520 or 0)
        if t2 > 0:
            template.row_600 = t2
    
    # Auto-calculate Total Own Funds
    if template.row_700 is None:
        t1 = template.row_400 or 0
        t2 = template.row_600 or 0
        if t1 > 0 or t2 > 0:
            template.row_700 = t1 + t2
    
    return template
