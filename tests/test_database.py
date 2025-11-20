#!/usr/bin/env python3
"""Test database loading and operations."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database import ComponentDatabase

def test_database():
    """Test database loading and basic operations."""
    print("Testing Component Database...")
    print("-" * 50)
    
    try:
        # Load database
        db = ComponentDatabase()
        print(f"✓ Database loaded: {db.count()} components")
        
        # Test search
        results = db.search_by_query("WiFi microcontroller")
        print(f"✓ Search 'WiFi microcontroller': {len(results)} results")
        if results:
            print(f"  First result: {results[0].mpn} - {results[0].manufacturer}")
        
        # Test get by MPN
        component = db.get_by_mpn("ESP32-S3-WROOM-1-N8R2")
        if component:
            print(f"✓ Get by MPN: {component.mpn} - {component.description[:50]}...")
        
        # Test categories
        categories = db.get_all_categories()
        print(f"✓ Categories: {', '.join(categories)}")
        
        # Test compatibility
        compat = db.check_compatibility(["ESP32-S3-WROOM-1-N8R2", "BME280"])
        print(f"✓ Compatibility check: {compat['compatible']}")
        
        print("-" * 50)
        print("All tests passed! ✓")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)

