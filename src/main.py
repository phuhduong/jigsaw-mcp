#!/usr/bin/env python3
"""MCP server for electronic component database."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Dict, List

from openmcp import MCPServer, tool

from .tools.component_tools import (
    initialize_database,
    search_components_tool,
    get_component_details_tool,
    check_compatibility_tool,
    suggest_alternatives_tool,
)

# Initialize database
data_file = os.getenv(
    "COMPONENT_DB_PATH",
    str(Path(__file__).parent / "data" / "components.json")
)
initialize_database(data_file)

# Create server instance
server = MCPServer("jigsaw-component-server")

# Register tools
with server.binding():

    @tool(description="Search for electronic components by natural language query")
    def search_components(query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for electronic components by natural language query."""
        return search_components_tool(query, limit)

    @tool(description="Get detailed specifications for a component by its MPN")
    def get_component_details(mpn: str) -> Dict[str, Any]:
        """Get detailed specifications for a component by its MPN."""
        return get_component_details_tool(mpn)

    @tool(description="Check compatibility between multiple components")
    def check_compatibility(mpns: List[str]) -> Dict[str, Any]:
        """Check compatibility between multiple components."""
        return check_compatibility_tool(mpns)

    @tool(description="Get alternative or similar components for a given MPN")
    def suggest_alternatives(mpn: str) -> Dict[str, Any]:
        """Get alternative or similar components for a given MPN."""
        return suggest_alternatives_tool(mpn)


async def main() -> None:
    """Start the MCP server."""
    await server.serve(transport="streamable-http", verbose=False, log_level="critical")


if __name__ == "__main__":
    asyncio.run(main())
