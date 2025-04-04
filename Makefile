.PHONY: install clean run test setup

install:
	pip install -r requirements.txt

setup:
	mkdir -p chroma_data

clean:
	rm -rf chroma_data
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete

run:
	python main.py

test:
	pytest tests/ 