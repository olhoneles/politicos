run:
	@python server.py

setup:
	@pip install -r requirements.txt -r requirements_dev.txt

setup-prod:
	@pip install -r requirements.txt

lint:
	@flake8

test: coverage lint

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests

focus:
	@coverage run --branch `which nosetests` -vv --with-yanc --with-focus -s tests

coverage: unit
	@coverage report -m

coverage-html: coverage
	@coverage html

collect:
	@python collector.py

clean_pycs:
	@find . -name "*.pyc" -delete
	@find . -type d -name __pycache__ -delete
