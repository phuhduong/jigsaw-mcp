#!/usr/bin/env python3
"""Root entry point for Dedalus deployment."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the server
if __name__ == "__main__":
    from src.main import main
    import asyncio
    asyncio.run(main())
