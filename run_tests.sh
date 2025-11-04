#!/bin/bash
# run_tests.sh - Script to run all tests for datasync library

set -e  # Exit on error

echo "========================================="
echo "DataSync Library - Test Runner"
echo "========================================="

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run setup.sh first to create the environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest is not installed."
    echo "Please run setup.sh to install dependencies."
    exit 1
fi

echo ""
echo "Running tests..."
echo "========================================="
echo ""

# Run pytest with verbose output and coverage
pytest test_files/ \
    -v \
    --tb=short \
    --color=yes \
    -ra

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "========================================="

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed successfully!"
else
    echo "✗ Some tests failed. Please review the output above."
fi

echo "========================================="
echo ""

# Exit with the test exit code
exit $TEST_EXIT_CODE
