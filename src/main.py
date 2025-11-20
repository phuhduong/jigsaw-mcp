"""
Main MCP server implementation.
Uses openmcp framework for Dedalus deployment.
"""

import os
import asyncio
from pathlib import Path
from typing import Any, Dict, List

# Import openmcp framework
# Dedalus provides openmcp automatically when 'mcp' is in dependencies
# For local development: run 'uv sync' to install dependencies
from openmcp import MCPServer, tool

from .tools.component_tools import (
    initialize_database,
    search_components_tool,
    get_component_details_tool,
    check_compatibility_tool,
    suggest_alternatives_tool,
)

# Initialize database on module load
data_file = os.getenv(
    "COMPONENT_DB_PATH",
    str(Path(__file__).parent / "data" / "components.json")
)
initialize_database(data_file)

# Create MCP server instance
server = MCPServer("jigsaw-component-server")

# Register tools using openmcp's binding context
# This pattern matches the Dedalus template
with server.binding():
    
    @tool(description="Search for electronic components by natural language query")
    def search_components(query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search for electronic components by natural language query.
        
        Args:
            query: Natural language search query (e.g., "WiFi microcontroller", "temperature sensor")
            limit: Maximum number of results (default: 10)
        
        Returns:
            Dictionary with search results including component MPNs, descriptions, and prices
        """
        return search_components_tool(query, limit)
    
    @tool(description="Get detailed specifications for a component by its MPN")
    def get_component_details(mpn: str) -> Dict[str, Any]:
        """
        Get detailed specifications for a component by its MPN (Manufacturer Part Number).
        
        Args:
            mpn: Manufacturer Part Number (e.g., "ESP32-S3-WROOM-1-N8R2")
        
        Returns:
            Dictionary with full component details including specs, pricing, and datasheet URL
        """
        return get_component_details_tool(mpn)
    
    @tool(description="Check compatibility between multiple components")
    def check_compatibility(mpns: List[str]) -> Dict[str, Any]:
        """
        Check compatibility between multiple components.
        Validates voltage ranges, interface requirements, and other compatibility factors.
        
        Args:
            mpns: List of MPNs to check compatibility for
        
        Returns:
            Compatibility report with any issues found
        """
        return check_compatibility_tool(mpns)
    
    @tool(description="Get alternative or similar components for a given MPN")
    def suggest_alternatives(mpn: str) -> Dict[str, Any]:
        """
        Get alternative or similar components for a given MPN.
        Useful when a component is out of stock or needs replacement.
        
        Args:
            mpn: Manufacturer Part Number
        
        Returns:
            Dictionary with list of alternative components
        """
        return suggest_alternatives_tool(mpn)


async def main() -> None:
    """Start the MCP server on streamable-http transport."""
    print("🚀 Starting Jigsaw Component MCP Server...")
    print("📡 Transport: streamable-http")
    print("🔧 Available tools: search_components, get_component_details, check_compatibility, suggest_alternatives")
    print()
    await server.serve(transport="streamable-http", verbose=False, log_level="critical")


if __name__ == "__main__":
    asyncio.run(main())

