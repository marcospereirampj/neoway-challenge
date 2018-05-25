# Challenge Makefile

start:
# commands

check:
	python -m unittest discover -s api -p "*_test.py"

requirements: api/requirements.txt
	pip install -r api/requirements.txt
