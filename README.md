# Jigsaw MCP Server - Component Database

MCP server with embedded component database for electronic component search and analysis.

## Features

- **Embedded Component Database**: 100+ electronic components (MCUs, sensors, power management, etc.)
- **Component Search**: Natural language search for components
- **Component Details**: Get full specifications by MPN
- **Compatibility Checking**: Validate component compatibility
- **Alternative Suggestions**: Find similar/replacement components

## Installation

### Prerequisites

- Python 3.10+
- `uv` package manager (required for Dedalus deployment)

### Setup

1. **Install uv** (same as Dedalus uses):

```bash
brew install uv  # macOS
# or
pip install uv  # Other platforms
```

2. **Install dependencies**:

```bash
cd mcp_server
uv sync --no-dev
```

This installs dependencies from `pyproject.toml` (required for Dedalus).

## Project Structure

```
mcp_server/
├── main.py                  # Root entry point (required by Dedalus)
├── pyproject.toml          # Package configuration and dependencies
├── src/
│   ├── main.py             # MCP server implementation
│   ├── tools/
│   │   └── component_tools.py  # MCP tool implementations
│   ├── database/
│   │   ├── loader.py       # Database loading and search
│   │   └── models.py       # Component data models
│   └── data/
│       └── components.json  # Embedded component database
├── tests/                  # Test suite
│   ├── test_database.py
│   ├── test_tools.py
│   ├── test_server.py
│   ├── test_dedalus_structure.py
│   └── run_all_tests.py
├── run_tests.sh            # Test runner script
└── README.md
```

## MCP Tools

The server exposes the following tools:

### 1. `search_components`
Search for components by natural language query.

**Parameters:**
- `query` (str): Search query (e.g., "WiFi microcontroller", "temperature sensor")
- `limit` (int, optional): Max results (default: 10)

**Returns:** List of matching components with basic info

### 2. `get_component_details`
Get detailed specifications for a component by MPN.

**Parameters:**
- `mpn` (str): Manufacturer Part Number

**Returns:** Full component details including specs, pricing, datasheet

### 3. `check_compatibility`
Check compatibility between multiple components.

**Parameters:**
- `mpns` (list[str]): List of MPNs to check

**Returns:** Compatibility report with voltage, interface checks

### 4. `suggest_alternatives`
Get alternative components for a given MPN.

**Parameters:**
- `mpn` (str): Manufacturer Part Number

**Returns:** List of alternative components

## Local Development

### Testing

The project includes comprehensive test scripts to verify functionality before deployment:

1. **Run all tests** (recommended):

```bash
cd mcp_server
./run_tests.sh
```

This runs:
- Database loading and search tests
- MCP tool functionality tests
- Server setup and tool registration tests

2. **Run individual tests**:

```bash
# Test database only
python3 tests/test_database.py

# Test MCP tools
python3 tests/test_tools.py

# Test server setup
python3 tests/test_server.py

# Test Dedalus structure compliance
python3 tests/test_dedalus_structure.py
```

3. **Test the server locally** (using uv, same as Dedalus):

```bash
# Install dependencies
uv sync --no-dev

# Run server (same command Dedalus uses)
uv run main
```

4. **Manual database testing**:

```python
from src.database import ComponentDatabase

db = ComponentDatabase()
results = db.search_by_query("WiFi microcontroller")
print(results)
```

## Deployment to Dedalus Labs

### Prerequisites

- Code pushed to GitHub repository
- `pyproject.toml` present (✅ included)
- `main.py` (root) - Entry point that Dedalus expects (✅ included)
- `src/main.py` - The actual MCP server code (✅ included)

### Deployment Steps

1. **Push to GitHub**: Ensure your code is in a GitHub repository

2. **Deploy via Dedalus Dashboard**:
   - Connect your GitHub repository
   - Dedalus will:
     - Run `uv sync` to install dependencies from `pyproject.toml`
     - Run `uv run main` to start the server (executes `src.main:main` directly)
     - Auto-detect the server structure
   - Configure any environment variables if needed (e.g., `COMPONENT_DB_PATH`)

3. **Get MCP Server URL**: Dedalus will provide the server URL after deployment

### How Dedalus Runs Your Server

1. **Build Phase**:
   - Reads `pyproject.toml`
   - Runs `uv sync` to install dependencies (installs `mcp`, Dedalus provides `openmcp` automatically)
   - Creates container environment

2. **Runtime**:
   - Working directory: `/app`
   - Runs: `uv run main` (executes root `main.py`, which calls `src.main.main()`)
   - Communicates via streamable-http protocol

3. **File Access**:
   - Your files are in `/app/`
   - Component database in `/app/src/data/components.json`
   - Use absolute paths or Path objects

### Key Alignment with Template

This server follows the Dedalus framework requirements:
- Uses `"mcp"` in `pyproject.toml` (Dedalus provides `openmcp` automatically)
- Has root `main.py` entry point (as required by Dedalus)
- Entry point in `pyproject.toml`: `"src.main:main"` (points to actual server code)
- Uses `from openmcp import MCPServer, tool` in code
- Server instance named `server` (matches template)

## Environment Variables

- `COMPONENT_DB_PATH`: Path to component database JSON file (optional, defaults to `src/data/components.json`)

## Adding Components

To add more components, edit `src/data/components.json`:

```json
{
  "components": [
    {
      "mpn": "PART-NUMBER",
      "manufacturer": "Manufacturer Name",
      "category": "MCU|Sensor|Power|Memory|RF|Connector|Passive|Display",
      "description": "Component description",
      "specs": {
        "voltage_min": 3.0,
        "voltage_max": 3.6,
        "current_max": 0.24,
        "package": "48-QFN",
        "interfaces": ["I2C", "SPI"],
        "pin_count": 48
      },
      "pricing": {
        "price_usd": 2.89,
        "currency": "USD",
        "stock_status": "in_stock"
      },
      "datasheet_url": "https://...",
      "compatibility": {
        "voltage_compatible": [3.0, 3.3, 3.6],
        "interface_requirements": ["I2C"]
      },
      "alternatives": ["ALT-MPN-1", "ALT-MPN-2"]
    }
  ]
}
```

## Notes

- Database is loaded into memory on server startup for fast queries
- Current database has ~20 components (expandable to 100-200+)
- All tools are stateless and don't require authentication
- Compatible with Dedalus Labs MCP gateway

## License

Part of the Jigsaw project.

