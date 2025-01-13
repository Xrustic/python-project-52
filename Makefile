dev:
	python3 manage.py runserver 0.0.0.0:8000
PORT ?= 8000
gunicorn:
	poetry run gunicorn -w 4 -b 0.0.0.0:$(PORT) task_manager.asgi:application -k uvicorn.workers.UvicornWorker

install:
	poetry install

build:
	./build.sh

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 task_manager --exclude .git,__pycache__,docs/source/conf.py,old,build,dist,*/migrations

test:
	poetry run pytest --cov=task_manager

test-coverage:
	poetry run python3 -m pytest --cov=task_manager --cov-report=xml:coverage.xml
