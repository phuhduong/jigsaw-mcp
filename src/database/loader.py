"""Component database loader and search functionality."""

import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from .models import Component


class ComponentDatabase:
    """In-memory component database with search capabilities."""
    
    def __init__(self, data_file: Optional[str] = None):
        """Initialize database from JSON file."""
        if data_file is None:
            # Default to components.json in data directory
            current_dir = Path(__file__).parent.parent
            data_file = current_dir / "data" / "components.json"
        
        self.data_file = Path(data_file)
        self.components: List[Component] = []
        self._load_components()
    
    def _load_components(self) -> None:
        """Load components from JSON file."""
        if not self.data_file.exists():
            raise FileNotFoundError(f"Component database not found: {self.data_file}")
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.components = [
            Component.from_dict(comp_data)
            for comp_data in data.get("components", [])
        ]
    
    def search_by_query(self, query: str, limit: int = 10) -> List[Component]:
        """
        Search components by natural language query.
        Searches in MPN, manufacturer, category, description, and interfaces.
        """
        query_lower = query.lower()
        results = []
        
        for component in self.components:
            score = 0
            
            # Exact MPN match (highest priority)
            if query_lower in component.mpn.lower():
                score += 100
            
            # Manufacturer match
            if query_lower in component.manufacturer.lower():
                score += 50
            
            # Category match
            if query_lower in component.category.lower():
                score += 30
            
            # Description match
            if query_lower in component.description.lower():
                score += 20
            
            # Interface match
            for interface in component.specs.interfaces:
                if query_lower in interface.lower():
                    score += 15
            
            # Keyword matching
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in component.description.lower():
                    score += 5
                if keyword in component.category.lower():
                    score += 10
            
            if score > 0:
                results.append((score, component))
        
        # Sort by score (descending) and return top results
        results.sort(key=lambda x: x[0], reverse=True)
        return [comp for _, comp in results[:limit]]
    
    def search_by_category(self, category: str, limit: int = 20) -> List[Component]:
        """Search components by category."""
        category_lower = category.lower()
        results = [
            comp for comp in self.components
            if category_lower in comp.category.lower()
        ]
        return results[:limit]
    
    def get_by_mpn(self, mpn: str) -> Optional[Component]:
        """Get component by MPN (exact match)."""
        for component in self.components:
            if component.mpn.upper() == mpn.upper():
                return component
        return None
    
    def get_alternatives(self, mpn: str) -> List[Component]:
        """Get alternative components for a given MPN."""
        component = self.get_by_mpn(mpn)
        if not component:
            return []
        
        alternatives = []
        for alt_mpn in component.alternatives:
            alt_comp = self.get_by_mpn(alt_mpn)
            if alt_comp:
                alternatives.append(alt_comp)
        
        return alternatives
    
    def check_compatibility(self, mpns: List[str]) -> Dict[str, Any]:
        """
        Check compatibility between multiple components.
        Returns compatibility report with voltage, interface, and other checks.
        """
        components = [self.get_by_mpn(mpn) for mpn in mpns]
        components = [c for c in components if c is not None]
        
        if len(components) < 2:
            return {
                "compatible": True,
                "message": "Need at least 2 components to check compatibility",
                "issues": []
            }
        
        issues = []
        
        # Check voltage compatibility
        voltage_ranges = []
        for comp in components:
            if comp.specs.voltage_min and comp.specs.voltage_max:
                voltage_ranges.append((comp.specs.voltage_min, comp.specs.voltage_max))
        
        if voltage_ranges:
            min_voltage = max(v[0] for v in voltage_ranges)
            max_voltage = min(v[1] for v in voltage_ranges)
            
            if min_voltage > max_voltage:
                issues.append({
                    "type": "voltage",
                    "severity": "error",
                    "message": f"Voltage ranges incompatible: {voltage_ranges}"
                })
        
        # Check interface compatibility (if components require specific interfaces)
        required_interfaces = set()
        provided_interfaces = set()
        
        for comp in components:
            if comp.specs.interfaces:
                provided_interfaces.update(comp.specs.interfaces)
                # Check if component requires specific interfaces from compatibility field
                if "interface_requirements" in comp.compatibility:
                    required_interfaces.update(comp.compatibility["interface_requirements"])
        
        # Check if all required interfaces are available
        missing_interfaces = required_interfaces - provided_interfaces
        if missing_interfaces:
            issues.append({
                "type": "interface",
                "severity": "warning",
                "message": f"Missing required interfaces: {missing_interfaces}"
            })
        
        return {
            "compatible": len(issues) == 0 or all(i["severity"] != "error" for i in issues),
            "components": [c.mpn for c in components],
            "issues": issues,
            "voltage_range": {
                "min": min_voltage if voltage_ranges else None,
                "max": max_voltage if voltage_ranges else None
            } if voltage_ranges else None,
            "available_interfaces": list(provided_interfaces)
        }
    
    def get_all_categories(self) -> List[str]:
        """Get list of all unique categories."""
        return sorted(set(comp.category for comp in self.components))
    
    def count(self) -> int:
        """Get total number of components."""
        return len(self.components)

