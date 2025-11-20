"""MCP tools for component database operations."""

from typing import Any, Dict, List
from ..database import ComponentDatabase
from ..database.models import Component


# Global database instance (loaded on server startup)
_db: ComponentDatabase = None


def initialize_database(data_file: str = None) -> None:
    """Initialize the component database."""
    global _db
    _db = ComponentDatabase(data_file)


def search_components_tool(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search for components by natural language query.
    
    Args:
        query: Natural language search query (e.g., "WiFi microcontroller", "temperature sensor")
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        Dictionary with search results
    """
    if _db is None:
        raise RuntimeError("Database not initialized")
    
    results = _db.search_by_query(query, limit)
    
    return {
        "query": query,
        "count": len(results),
        "components": [
            {
                "mpn": comp.mpn,
                "manufacturer": comp.manufacturer,
                "category": comp.category,
                "description": comp.description,
                "price_usd": comp.pricing.price_usd,
                "interfaces": comp.specs.interfaces,
            }
            for comp in results
        ]
    }


def get_component_details_tool(mpn: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific component by MPN.
    
    Args:
        mpn: Manufacturer Part Number (e.g., "ESP32-S3-WROOM-1-N8R2")
    
    Returns:
        Dictionary with full component details
    """
    if _db is None:
        raise RuntimeError("Database not initialized")
    
    component = _db.get_by_mpn(mpn)
    
    if not component:
        return {
            "found": False,
            "mpn": mpn,
            "message": f"Component {mpn} not found in database"
        }
    
    return {
        "found": True,
        "mpn": component.mpn,
        "manufacturer": component.manufacturer,
        "category": component.category,
        "description": component.description,
        "specs": {
            "voltage_min": component.specs.voltage_min,
            "voltage_max": component.specs.voltage_max,
            "voltage_out": component.specs.voltage_out,
            "current_max": component.specs.current_max,
            "package": component.specs.package,
            "interfaces": component.specs.interfaces,
            "pin_count": component.specs.pin_count,
            "flash_memory_mb": component.specs.flash_memory_mb,
            "ram_mb": component.specs.ram_mb,
        },
        "pricing": {
            "price_usd": component.pricing.price_usd,
            "currency": component.pricing.currency,
            "stock_status": component.pricing.stock_status,
        },
        "datasheet_url": component.datasheet_url,
        "compatibility": component.compatibility,
        "alternatives": component.alternatives,
    }


def check_compatibility_tool(mpns: List[str]) -> Dict[str, Any]:
    """
    Check compatibility between multiple components.
    
    Args:
        mpns: List of MPNs to check compatibility for
    
    Returns:
        Compatibility report with any issues found
    """
    if _db is None:
        raise RuntimeError("Database not initialized")
    
    return _db.check_compatibility(mpns)


def suggest_alternatives_tool(mpn: str) -> Dict[str, Any]:
    """
    Get alternative/similar components for a given MPN.
    
    Args:
        mpn: Manufacturer Part Number
    
    Returns:
        Dictionary with list of alternative components
    """
    if _db is None:
        raise RuntimeError("Database not initialized")
    
    component = _db.get_by_mpn(mpn)
    
    if not component:
        return {
            "found": False,
            "mpn": mpn,
            "message": f"Component {mpn} not found in database",
            "alternatives": []
        }
    
    alternatives = _db.get_alternatives(mpn)
    
    return {
        "found": True,
        "mpn": mpn,
        "original": {
            "mpn": component.mpn,
            "manufacturer": component.manufacturer,
            "category": component.category,
        },
        "alternatives": [
            {
                "mpn": alt.mpn,
                "manufacturer": alt.manufacturer,
                "category": alt.category,
                "description": alt.description,
                "price_usd": alt.pricing.price_usd,
            }
            for alt in alternatives
        ]
    }

