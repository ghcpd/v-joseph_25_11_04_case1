#!/bin/bash
# setup.sh - Environment setup script for datasync library

set -e  # Exit on error

echo "========================================="
echo "DataSync Library - Environment Setup"
echo "========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "Setting up virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "Warning: requirements.txt not found. Skipping dependency installation."
fi

# Verify pytest installation
echo ""
echo "Verifying pytest installation..."
if command -v pytest &> /dev/null; then
    PYTEST_VERSION=$(pytest --version)
    echo "✓ $PYTEST_VERSION"
else
    echo "✗ pytest not found. Installing pytest..."
    pip install pytest
fi

# Display installed packages
echo ""
echo "Installed packages:"
pip list | grep -E "pytest|pluggy|packaging|iniconfig"

echo ""
echo "========================================="
echo "Setup completed successfully!"
echo "========================================="
echo ""
echo "To activate the virtual environment manually, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run tests, execute:"
echo "  ./run_tests.sh"
echo "  or"
echo "  pytest test_files/"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
echo ""
