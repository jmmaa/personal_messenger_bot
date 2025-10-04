python3.11 -m venv .venv
call ".venv/Scripts/activate"
pip install build
python -m build
pip install -e .
