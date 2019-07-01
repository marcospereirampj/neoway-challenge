# Challenge Makefile

default:
	@echo "Running project:"
	@echo "    make start         # Starts a Flask development server locally (open http://localhost:5000/)."
	@echo "    make check         # Tests entire application."
	@echo "    make setup         # Install requirements."

start:
	PYTHONPATH=./api/ python api/run.py

check:
	PYTHONPATH=./api/ python -m unittest discover -p *tests.py

setup:
	pip install -r api/requirements.txt