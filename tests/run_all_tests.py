#!/usr/bin/env python3
"""
Run all tests to validate Dedalus MCP server.
"""

import sys
import subprocess
from pathlib import Path

def run_test(test_file: str) -> bool:
    """Run a single test file."""
    test_path = Path(__file__).parent / test_file
    print(f"\n{'='*60}")
    print(f"Running {test_file}...")
    print('='*60)
    
    result = subprocess.run(
        [sys.executable, str(test_path)],
        capture_output=False
    )
    
    return result.returncode == 0

def main():
    """Run all tests."""
    print("="*60)
    print("Jigsaw MCP Server - Complete Test Suite")
    print("Validating Dedalus Template Compliance")
    print("="*60)
    
    tests = [
        "test_database.py",
        "test_tools.py",
        "test_dedalus_structure.py",
        "test_server.py",
    ]
    
    results = {}
    
    for test_file in tests:
        results[test_file] = run_test(test_file)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_file, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_file}")
        if not passed:
            all_passed = False
    
    print("="*60)
    if all_passed:
        print("🎉 All tests passed! Server is ready for Dedalus deployment.")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

