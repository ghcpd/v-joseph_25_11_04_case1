# Task: Incorrect Documentation Verification

You are provided with a Python library `datasync` containing three modules: `sync.py`, `config.py`, and `metrics.py`.

The `README.md` and inline docstrings may contain incorrect or outdated information.

Your goal is to:

1. Follow the README instructions as written and execute all code examples.
2. Detect inconsistencies between the documentation and actual implementation, including:
   - Wrong parameter names
   - Outdated or incorrect defaults
   - Invalid value ranges
   - Missing or renamed arguments
   - Mismatched return values or attributes
   - Contradictory information across files
3. Generate the following files:
   - `defects.txt`: full list of detected inconsistencies with references
   - `corrected_readme.md`: fully corrected version of README
   - `requirements.txt` - Add required the libraries based on the .venv 
   - `setup.sh` - Bash file to setup the environment 
   - `test_files` - Test files to see if evertthing goes well 
   - `run_tests.sh` - Test command to run testcases

Environment: use `.venv` and `pytest` for validation.