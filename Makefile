.PHONY: install run test clean docker-build docker-run

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && python3 app.py

test:
	. venv/bin/activate && python -m pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf venv

docker-build:
	docker compose build

docker-run:
	docker compose up -d
