call ".venv/Scripts/Activate"
call python3.11 -m pip install build
call python3.11 -m build
call python3.11 -m pip install -e .
