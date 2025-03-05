PORT ?= 8000
install:
	pip install uv
	uv pip install -r requirements.txt

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh 

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app