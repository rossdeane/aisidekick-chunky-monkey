.PHONY: install clean run test setup

install:
	pip3 install -r requirements.txt

setup:
	mkdir -p chroma_data

clean:
	rm -rf chroma_data
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete

run:
	python3 main.py

test:
	pytest tests/ 