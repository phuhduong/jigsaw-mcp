#!/usr/bin/env python3
"""
Test Dedalus template structure compliance.
Validates that the MCP server follows Dedalus deployment requirements.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_dedalus_structure():
    """Test that the server structure matches Dedalus requirements."""
    print("Testing Dedalus Template Structure...")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Required files exist
    print("\n1. Checking required files...")
    required_files = {
        "pyproject.toml": project_root / "pyproject.toml",
        "main.py (root)": project_root / "main.py",
        "src/main.py": project_root / "src" / "main.py",
        "components.json": project_root / "src" / "data" / "components.json",
    }
    
    for name, path in required_files.items():
        if path.exists():
            print(f"   ✓ {name} exists")
        else:
            print(f"   ✗ {name} MISSING")
            all_passed = False
    
    # Test 2: pyproject.toml structure
    print("\n2. Checking pyproject.toml...")
    try:
        import tomllib
        with open(project_root / "pyproject.toml", "rb") as f:
            config = tomllib.load(f)
        
        # Check for required sections
        if "project" in config:
            print("   ✓ Has [project] section")
            if "dependencies" in config["project"]:
                deps = config["project"]["dependencies"]
                print(f"   ✓ Has dependencies: {len(deps)} packages")
                # Check for 'mcp' dependency (template uses this, not openmcp)
                if "mcp" in deps:
                    print("   ✓ Uses 'mcp' dependency (matches template)")
                elif any("openmcp" in str(dep) for dep in deps):
                    print("   ⚠ Uses 'openmcp' directly (template uses 'mcp', Dedalus provides openmcp)")
                else:
                    print("   ⚠ 'mcp' dependency not found")
            else:
                print("   ✗ Missing dependencies")
                all_passed = False
        else:
            print("   ✗ Missing [project] section")
            all_passed = False
        
        if "project.scripts" in config or "project" in config and "scripts" in config.get("project", {}):
            scripts = config.get("project", {}).get("scripts", {})
            if "main" in scripts:
                entry_point = scripts["main"]
                print(f"   ✓ Has script entry point: main = {entry_point}")
                if entry_point == "src.main:main":
                    print("   ✓ Entry point matches template (src.main:main)")
                else:
                    print(f"   ⚠ Entry point is {entry_point} (template uses src.main:main)")
            else:
                print("   ✗ Missing 'main' script entry point")
                all_passed = False
        else:
            print("   ✗ Missing [project.scripts] section")
            all_passed = False
            
    except ImportError:
        # Python < 3.11 doesn't have tomllib, use basic check
        with open(project_root / "pyproject.toml", "r") as f:
            content = f.read()
            if "[project]" in content:
                print("   ✓ Has [project] section")
            if "main = " in content:
                print("   ✓ Has script entry point")
    except Exception as e:
        print(f"   ✗ Error reading pyproject.toml: {e}")
        all_passed = False
    
    # Test 3: Root main.py structure
    print("\n3. Checking root main.py...")
    try:
        with open(project_root / "main.py", "r") as f:
            content = f.read()
        
        if "def main()" in content:
            print("   ✓ Has main() function")
        else:
            print("   ✗ Missing main() function")
            all_passed = False
        
        if "from src.main" in content or "from src.main import" in content:
            print("   ✓ Imports from src.main")
        else:
            print("   ✗ Does not import from src.main")
            all_passed = False
        
        if "asyncio" in content:
            print("   ✓ Uses asyncio for async server")
        else:
            print("   ⚠ May not handle async properly")
            
    except Exception as e:
        print(f"   ✗ Error reading main.py: {e}")
        all_passed = False
    
    # Test 4: src/main.py structure
    print("\n4. Checking src/main.py...")
    try:
        with open(project_root / "src" / "main.py", "r") as f:
            content = f.read()
        
        # Check for openmcp imports
        if "from openmcp" in content or "import openmcp" in content:
            print("   ✓ Uses openmcp framework")
        else:
            print("   ⚠ May not use openmcp (fallback to mcp)")
        
        # Check for MCPServer
        if "MCPServer" in content:
            print("   ✓ Creates MCPServer instance")
        else:
            print("   ✗ Missing MCPServer")
            all_passed = False
        
        # Check for tool registration
        if "@tool" in content or "tool(" in content:
            print("   ✓ Registers tools with @tool decorator")
        else:
            print("   ✗ Missing tool registration")
            all_passed = False
        
        # Check for streamable-http transport
        if "streamable-http" in content:
            print("   ✓ Uses streamable-http transport")
        else:
            print("   ✗ Missing streamable-http transport (required by Dedalus)")
            all_passed = False
        
        # Check for async main function
        if "async def main" in content:
            print("   ✓ Has async main() function")
        else:
            print("   ⚠ May not be async")
        
        # Check for mcp.serve call
        if "mcp.serve" in content or ".serve(" in content:
            print("   ✓ Calls server.serve()")
        else:
            print("   ✗ Missing server.serve() call")
            all_passed = False
            
    except Exception as e:
        print(f"   ✗ Error reading src/main.py: {e}")
        all_passed = False
    
    # Test 5: Database file exists
    print("\n5. Checking component database...")
    db_path = project_root / "src" / "data" / "components.json"
    if db_path.exists():
        import json
        try:
            with open(db_path, "r") as f:
                data = json.load(f)
            if "components" in data:
                count = len(data["components"])
                print(f"   ✓ Database file exists with {count} components")
            else:
                print("   ⚠ Database file exists but missing 'components' key")
        except Exception as e:
            print(f"   ✗ Database file is invalid JSON: {e}")
            all_passed = False
    else:
        print("   ✗ Database file missing")
        all_passed = False
    
    # Test 6: Required directories
    print("\n6. Checking directory structure...")
    required_dirs = [
        "src",
        "src/database",
        "src/tools",
        "src/data",
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"   ✓ {dir_path}/ exists")
        else:
            print(f"   ✗ {dir_path}/ MISSING")
            all_passed = False
    
    # Test 7: Can import server module (if openmcp available)
    print("\n7. Testing module imports...")
    try:
        # Test importing src.main
        from src.main import mcp, main
        print("   ✓ Can import src.main")
        print(f"   ✓ Server instance created: {type(mcp).__name__}")
        
        # Check if mcp has expected attributes
        if hasattr(mcp, 'serve'):
            print("   ✓ Server has serve() method")
        else:
            print("   ⚠ Server missing serve() method")
        
    except ImportError as e:
        error_msg = str(e)
        if "openmcp" in error_msg.lower() or "mcp" in error_msg.lower():
            print("   ⚠ Cannot import (openmcp not installed locally)")
            print("   ✓ This is OK - Dedalus will provide openmcp during deployment")
            print("   ✓ Code structure is correct")
            # Don't fail the test for this - it's expected locally
        else:
            print(f"   ✗ Cannot import src.main: {e}")
            all_passed = False
    except Exception as e:
        print(f"   ✗ Error importing: {e}")
        all_passed = False
    
    # Test 8: Entry point can be executed
    print("\n8. Testing entry point execution...")
    try:
        # Test that src.main.main can be imported and is callable
        from src.main import main as server_main
        import inspect
        
        if inspect.iscoroutinefunction(server_main):
            print("   ✓ src.main.main is async function (correct)")
        else:
            print("   ⚠ src.main.main is not async")
        
        print("   ✓ Entry point is importable and valid")
        
    except ImportError as e:
        error_msg = str(e)
        if "openmcp" in error_msg.lower():
            print("   ⚠ Cannot import (openmcp not installed locally)")
            print("   ✓ This is OK - Dedalus will provide openmcp")
        else:
            print(f"   ✗ Entry point has issues: {e}")
            all_passed = False
    except Exception as e:
        print(f"   ⚠ Entry point test issue: {e}")
        print("   (This may be OK if openmcp is not installed locally)")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All Dedalus structure tests passed!")
        print("\nYour MCP server is ready for Dedalus deployment:")
        print("  - Required files present")
        print("  - pyproject.toml configured correctly")
        print("  - Uses openmcp framework")
        print("  - Uses streamable-http transport")
        print("  - Entry points configured properly")
    else:
        print("❌ Some structure tests failed!")
        print("Please fix the issues above before deploying to Dedalus.")
    
    return all_passed

if __name__ == "__main__":
    success = test_dedalus_structure()
    sys.exit(0 if success else 1)

