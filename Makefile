.PHONY: init
init:
	pip install --upgrade pip
	pip install -r requirements.txt

.PHONY: lint
lint:
	black .
	flake8 .
	isort .
	mypy .

.PHONY: ngrok
ngrok:
	ngrok http 3000

.PHONY: run
run:
	python app.py
