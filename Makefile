.PHONY: init
init:
	test -f .env || cp .env.template .env
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
	gunicorn -w 2 -b 0.0.0.0:3000 app:app
