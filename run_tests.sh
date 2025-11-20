#!/bin/bash

echo "=========================================="
echo "Jigsaw MCP Server - Test Suite"
echo "=========================================="
echo ""

# Run all tests from tests/ directory
cd "$(dirname "$0")"
python3 tests/run_all_tests.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ All tests passed!"
    echo "Your MCP server is ready for Dedalus deployment!"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "❌ Some tests failed"
    echo "Please fix issues before deploying to Dedalus"
    echo "=========================================="
fi

exit $exit_code

