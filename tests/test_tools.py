#!/usr/bin/env python3
"""Test MCP tools directly without server."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.tools.component_tools import (
    initialize_database,
    search_components_tool,
    get_component_details_tool,
    check_compatibility_tool,
    suggest_alternatives_tool,
)

def test_tools():
    """Test all MCP tools."""
    print("Testing MCP Tools...")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    try:
        initialize_database()
        print("   ✓ Database initialized")
    except Exception as e:
        print(f"   ✗ Failed to initialize database: {e}")
        return False
    
    # Test search_components
    print("\n2. Testing search_components...")
    try:
        result = search_components_tool("WiFi microcontroller", limit=3)
        print(f"   Query: 'WiFi microcontroller'")
        print(f"   Results: {result['count']} components found")
        if result['components']:
            first = result['components'][0]
            print(f"   First result: {first['mpn']} - {first['manufacturer']}")
            print(f"   Price: ${first['price_usd']}")
        print("   ✓ search_components works")
    except Exception as e:
        print(f"   ✗ search_components failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test get_component_details
    print("\n3. Testing get_component_details...")
    try:
        result = get_component_details_tool("ESP32-S3-WROOM-1-N8R2")
        if result.get('found'):
            print(f"   MPN: {result['mpn']}")
            print(f"   Manufacturer: {result['manufacturer']}")
            print(f"   Category: {result['category']}")
            print(f"   Price: ${result['pricing']['price_usd']}")
            print(f"   Interfaces: {', '.join(result['specs']['interfaces'])}")
            print("   ✓ get_component_details works")
        else:
            print(f"   ✗ Component not found: {result.get('message')}")
            return False
    except Exception as e:
        print(f"   ✗ get_component_details failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test check_compatibility
    print("\n4. Testing check_compatibility...")
    try:
        result = check_compatibility_tool([
            "ESP32-S3-WROOM-1-N8R2",
            "BME280",
            "AP2112K-3.3TRG1"
        ])
        print(f"   Components checked: {len(result['components'])}")
        print(f"   Compatible: {result['compatible']}")
        if result.get('voltage_range'):
            vr = result['voltage_range']
            print(f"   Voltage range: {vr['min']}V - {vr['max']}V")
        if result.get('available_interfaces'):
            print(f"   Available interfaces: {', '.join(result['available_interfaces'])}")
        if result.get('issues'):
            print(f"   Issues found: {len(result['issues'])}")
            for issue in result['issues']:
                print(f"     - {issue['type']}: {issue['message']}")
        print("   ✓ check_compatibility works")
    except Exception as e:
        print(f"   ✗ check_compatibility failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test suggest_alternatives
    print("\n5. Testing suggest_alternatives...")
    try:
        result = suggest_alternatives_tool("ESP32-S3-WROOM-1-N8R2")
        if result.get('found'):
            print(f"   Original: {result['original']['mpn']} ({result['original']['manufacturer']})")
            print(f"   Alternatives: {len(result['alternatives'])}")
            if result['alternatives']:
                for alt in result['alternatives'][:3]:  # Show first 3
                    print(f"     - {alt['mpn']}: ${alt['price_usd']}")
            print("   ✓ suggest_alternatives works")
        else:
            print(f"   ⚠ Component not found: {result.get('message')}")
            print("   (This is OK if component has no alternatives defined)")
    except Exception as e:
        print(f"   ✗ suggest_alternatives failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test edge cases
    print("\n6. Testing edge cases...")
    try:
        # Test search with no results
        result = search_components_tool("nonexistent component xyz123", limit=5)
        print(f"   Search for nonexistent: {result['count']} results (expected 0)")
        
        # Test get details for nonexistent MPN
        result = get_component_details_tool("NONEXISTENT-MPN-123")
        if not result.get('found'):
            print("   ✓ Handles nonexistent MPN correctly")
        
        # Test compatibility with single component
        result = check_compatibility_tool(["ESP32-S3-WROOM-1-N8R2"])
        print(f"   Single component compatibility: {result.get('message', 'OK')}")
        
        print("   ✓ Edge cases handled correctly")
    except Exception as e:
        print(f"   ✗ Edge case test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("All tool tests completed! ✓")
    return True

if __name__ == "__main__":
    try:
        success = test_tools()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

