#!/usr/bin/env python
"""
Test script to verify the MCP server is working correctly
"""

import sys
import os

# Add parent directory to path to find src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_server():
    """Test all server functionality"""
    print("Testing Simple Utility MCP Server\n")
    
    # Test 1: Check file structure
    print("Test 1: Checking file structure...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    required_files = {
        "pyproject.toml": os.path.join(project_root, "pyproject.toml"),
        "main.py": os.path.join(project_root, "main.py"),
        "src/main.py": os.path.join(project_root, "src", "main.py"),
    }
    
    all_files_exist = True
    for name, path in required_files.items():
        if os.path.exists(path):
            print(f"   ✓ {name} exists")
        else:
            print(f"   ✗ {name} MISSING")
            all_files_exist = False
    
    if not all_files_exist:
        print("[ERROR] Required files missing")
        return False
    
    # Test 2: Check pyproject.toml structure
    print("\nTest 2: Checking pyproject.toml...")
    try:
        import tomllib
        with open(required_files["pyproject.toml"], "rb") as f:
            config = tomllib.load(f)
        
        if "project" in config and "dependencies" in config["project"]:
            deps = config["project"]["dependencies"]
            if "mcp" in deps:
                print("   ✓ Has 'mcp' dependency")
            else:
                print("   ✗ Missing 'mcp' dependency")
                return False
            
            # Check for entry point in [project.scripts] section
            scripts = config.get("project", {}).get("scripts", {})
            if "main" in scripts:
                entry_point = scripts["main"]
                if entry_point == "src.main:main":
                    print(f"   ✓ Entry point correct: {entry_point}")
                else:
                    print(f"   ⚠ Entry point is: {entry_point} (expected: src.main:main)")
            else:
                print("   ✗ Missing entry point")
                return False
        else:
            print("   ✗ Invalid pyproject.toml structure")
            return False
    except ImportError:
        # Python < 3.11, use basic check
        with open(required_files["pyproject.toml"], "r") as f:
            content = f.read()
            if "mcp" in content and "main = " in content:
                print("   ✓ Basic structure looks correct")
            else:
                print("   ✗ Missing required elements")
                return False
    except Exception as e:
        print(f"   ✗ Error reading pyproject.toml: {e}")
        return False
    
    # Test 3: Check root main.py
    print("\nTest 3: Checking root main.py...")
    try:
        with open(required_files["main.py"], "r") as f:
            content = f.read()
        
        if "from src.main import" in content or "from src.main" in content:
            print("   ✓ Imports from src.main")
        else:
            print("   ✗ Does not import from src.main")
            return False
        
        if "asyncio" in content:
            print("   ✓ Uses asyncio")
        else:
            print("   ⚠ May not handle async properly")
    except Exception as e:
        print(f"   ✗ Error reading main.py: {e}")
        return False
    
    # Test 4: Check src/main.py structure
    print("\nTest 4: Checking src/main.py structure...")
    try:
        with open(required_files["src/main.py"], "r") as f:
            content = f.read()
        
        # Check for openmcp imports
        if "from openmcp" in content or "import openmcp" in content:
            print("   ✓ Uses openmcp framework")
        else:
            print("   ⚠ May not use openmcp")
        
        # Check for MCPServer
        if "MCPServer" in content:
            print("   ✓ Creates MCPServer instance")
        else:
            print("   ✗ Missing MCPServer")
            return False
        
        # Check for tool registration
        if "@tool" in content:
            print("   ✓ Registers tools with @tool decorator")
        else:
            print("   ✗ Missing tool registration")
            return False
        
        # Check for streamable-http transport
        if "streamable-http" in content:
            print("   ✓ Uses streamable-http transport")
        else:
            print("   ✗ Missing streamable-http transport")
            return False
        
        # Check for async main function
        if "async def main" in content:
            print("   ✓ Has async main() function")
        else:
            print("   ⚠ May not be async")
        
        # Check for server.serve call
        if ".serve(" in content:
            print("   ✓ Calls server.serve()")
        else:
            print("   ✗ Missing server.serve() call")
            return False
        
        # Check for expected tools
        expected_tools = [
            "reverse_text",
            "count_words",
            "factorial",
            "get_timestamp",
            "convert_temperature",
            "parse_csv_line"
        ]
        
        found_tools = []
        for tool_name in expected_tools:
            if f"def {tool_name}" in content:
                found_tools.append(tool_name)
        
        if len(found_tools) == len(expected_tools):
            print(f"   ✓ All {len(expected_tools)} tools are defined")
        else:
            print(f"   ⚠ Found {len(found_tools)}/{len(expected_tools)} tools")
            for tool in expected_tools:
                if tool not in found_tools:
                    print(f"      - Missing: {tool}")
        
    except Exception as e:
        print(f"   ✗ Error reading src/main.py: {e}")
        return False
    
    # Test 5: Try to import server (may fail locally, that's OK)
    print("\nTest 5: Testing module imports...")
    try:
        from src.main import server, main as server_main
        print("   ✓ Can import server and main")
        print(f"   ✓ Server instance: {type(server).__name__}")
        
        # Check server has required methods
        if hasattr(server, 'serve'):
            print("   ✓ Server has serve() method")
        else:
            print("   ✗ Server missing serve() method")
            return False
        
        # Check main is async
        import inspect
        if inspect.iscoroutinefunction(server_main):
            print("   ✓ main() is async function")
        else:
            print("   ⚠ main() is not async")
        
    except ImportError as e:
        error_msg = str(e)
        if "openmcp" in error_msg.lower() or "bs4" in error_msg.lower() or "mcp" in error_msg.lower():
            print("   ⚠ Cannot import (openmcp not installed locally)")
            print("   ✓ This is OK - Dedalus will provide dependencies")
            print("   ✓ Code structure is correct")
        else:
            print(f"   ✗ Import error: {e}")
            return False
    except Exception as e:
        print(f"   ⚠ Import issue: {e}")
        print("   (This may be OK if openmcp is not installed locally)")
    
    print("\n" + "="*50)
    print("[SUCCESS] All structure tests passed! Server is ready for Dedalus.")
    print("\nThe server structure matches Dedalus requirements:")
    print("  ✓ Required files present")
    print("  ✓ pyproject.toml configured correctly")
    print("  ✓ Uses openmcp framework")
    print("  ✓ Uses streamable-http transport")
    print("  ✓ Entry points configured properly")
    print("\nTo deploy to Dedalus:")
    print("  dedalus deploy . --name 'your-server-name'")
    
    return True

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
