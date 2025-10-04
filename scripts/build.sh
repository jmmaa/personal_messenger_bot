python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install build
python -m build
python -m pip install -e .
