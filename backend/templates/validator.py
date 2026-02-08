"""
Validation Engine - EBA-style validation rules for COREP templates
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from templates.c01_own_funds import C01OwnFundsTemplate, FIELD_METADATA


class ValidationResult(BaseModel):
    """Result of a single validation rule."""
    rule_id: str
    rule_name: str
    severity: str  # "ERROR" (blocking) or "WARNING" (non-blocking)
    passed: bool
    message: str
    affected_fields: List[str]


class ValidationEngine:
    """
    Validation engine implementing EBA-style validation rules.
    
    Rules are categorized by severity:
    - ERROR: Blocking rules that prevent submission
    - WARNING: Non-blocking but should be reviewed
    """
    
    def __init__(self):
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, List[Dict]]:
        """Load validation rules for each template type."""
        return {
            "C01": [
                # Consistency rules
                {
                    "id": "v0001",
                    "name": "CET1 Total Consistency",
                    "severity": "ERROR",
                    "check": self._check_cet1_total,
                    "description": "CET1 capital before adjustments must equal sum of CET1 components"
                },
                {
                    "id": "v0002",
                    "name": "Tier 1 Total Consistency",
                    "severity": "ERROR",
                    "check": self._check_tier1_total,
                    "description": "Tier 1 capital must equal CET1 + AT1"
                },
                {
                    "id": "v0003",
                    "name": "Total Own Funds Consistency",
                    "severity": "ERROR",
                    "check": self._check_total_own_funds,
                    "description": "Total own funds must equal Tier 1 + Tier 2"
                },
                {
                    "id": "v0004",
                    "name": "Non-Negative CET1",
                    "severity": "ERROR",
                    "check": self._check_non_negative_cet1,
                    "description": "CET1 capital cannot be negative"
                },
                # Warning rules
                {
                    "id": "v0010",
                    "name": "Missing CET1 Components",
                    "severity": "WARNING",
                    "check": self._check_cet1_components_present,
                    "description": "At least one CET1 component should be reported"
                },
                {
                    "id": "v0011",
                    "name": "Large AT1 Ratio",
                    "severity": "WARNING",
                    "check": self._check_at1_ratio,
                    "description": "AT1 should typically not exceed 1/3 of Tier 1 capital"
                },
                {
                    "id": "v0012",
                    "name": "Tier 2 Limit",
                    "severity": "WARNING",
                    "check": self._check_tier2_limit,
                    "description": "Tier 2 capital typically should not exceed Tier 1 capital"
                }
            ]
        }
    
    def validate(self, template: C01OwnFundsTemplate, template_type: str) -> List[Dict[str, Any]]:
        """Run all validation rules for a template."""
        results = []
        
        rules = self.rules.get(template_type, [])
        for rule in rules:
            check_fn = rule["check"]
            passed, message, affected = check_fn(template)
            
            results.append({
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "severity": rule["severity"],
                "passed": passed,
                "message": message if not passed else "OK",
                "affected_fields": affected,
                "description": rule["description"]
            })
        
        return results
    
    def get_rules(self, template_type: str) -> List[Dict[str, Any]]:
        """Get all rules for a template type."""
        rules = self.rules.get(template_type, [])
        return [{
            "id": r["id"],
            "name": r["name"],
            "severity": r["severity"],
            "description": r["description"]
        } for r in rules]
    
    # === Validation Check Functions ===
    
    def _check_cet1_total(self, t: C01OwnFundsTemplate) -> tuple:
        """Check that CET1 total equals sum of components."""
        components = [
            t.row_010 or 0,
            t.row_020 or 0,
            t.row_030 or 0,
            t.row_040 or 0,
            t.row_050 or 0,
            t.row_060 or 0,
            t.row_070 or 0
        ]
        expected = sum(components)
        actual = t.row_100 or 0
        
        if abs(actual - expected) > 0.01:  # Allow for rounding
            return (
                False,
                f"CET1 before adjustments ({actual:,.0f}) != sum of components ({expected:,.0f})",
                ["row_100", "row_010", "row_020", "row_030", "row_040", "row_050", "row_060"]
            )
        return (True, "", [])
    
    def _check_tier1_total(self, t: C01OwnFundsTemplate) -> tuple:
        """Check that Tier 1 equals CET1 + AT1."""
        cet1 = t.row_200 or 0
        at1 = t.row_300 or 0
        expected = cet1 + at1
        actual = t.row_400 or 0
        
        if abs(actual - expected) > 0.01:
            return (
                False,
                f"Tier 1 ({actual:,.0f}) != CET1 ({cet1:,.0f}) + AT1 ({at1:,.0f})",
                ["row_400", "row_200", "row_300"]
            )
        return (True, "", [])
    
    def _check_total_own_funds(self, t: C01OwnFundsTemplate) -> tuple:
        """Check total own funds consistency."""
        t1 = t.row_400 or 0
        t2 = t.row_600 or 0
        expected = t1 + t2
        actual = t.row_700 or 0
        
        if abs(actual - expected) > 0.01:
            return (
                False,
                f"Total own funds ({actual:,.0f}) != Tier 1 ({t1:,.0f}) + Tier 2 ({t2:,.0f})",
                ["row_700", "row_400", "row_600"]
            )
        return (True, "", [])
    
    def _check_non_negative_cet1(self, t: C01OwnFundsTemplate) -> tuple:
        """Check that CET1 is non-negative."""
        cet1 = t.row_200 or 0
        if cet1 < 0:
            return (
                False,
                f"CET1 capital is negative: {cet1:,.0f}",
                ["row_200"]
            )
        return (True, "", [])
    
    def _check_cet1_components_present(self, t: C01OwnFundsTemplate) -> tuple:
        """Check that at least one CET1 component is present."""
        components = [t.row_010, t.row_020, t.row_030, t.row_040, t.row_050, t.row_060]
        if all(c is None or c == 0 for c in components):
            return (
                False,
                "No CET1 capital components reported",
                ["row_010", "row_020", "row_030", "row_040", "row_050", "row_060"]
            )
        return (True, "", [])
    
    def _check_at1_ratio(self, t: C01OwnFundsTemplate) -> tuple:
        """Check AT1 ratio is reasonable."""
        at1 = t.row_300 or 0
        t1 = t.row_400 or 0
        
        if t1 > 0 and at1 > 0:
            ratio = at1 / t1
            if ratio > 0.33:
                return (
                    False,
                    f"AT1 is {ratio:.1%} of Tier 1 (typically should be ≤33%)",
                    ["row_300", "row_400"]
                )
        return (True, "", [])
    
    def _check_tier2_limit(self, t: C01OwnFundsTemplate) -> tuple:
        """Check Tier 2 doesn't exceed Tier 1."""
        t1 = t.row_400 or 0
        t2 = t.row_600 or 0
        
        if t2 > t1 and t1 > 0:
            return (
                False,
                f"Tier 2 ({t2:,.0f}) exceeds Tier 1 ({t1:,.0f})",
                ["row_600", "row_400"]
            )
        return (True, "", [])
