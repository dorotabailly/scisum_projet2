poetry env use 3.8
source .venv/bin/activate
poetry install
export PYTHONPATH="$PYTHONPATH:$(pwd)"
