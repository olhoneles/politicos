setup:
	@pip install -U --process-dependency-links  -e .\[tests\]

run:
	@python manage.py runserver 0.0.0.0:8000

data:
	@python manage.py syncdb

initial_data:
	@python manage.py countries
	@python manage.py states
	@python manage.py ethnicity
	@python manage.py education
	@python manage.py political_party
	@python manage.py mandate_event_type
	@python manage.py political_office
	@python manage.py institutions
	@python manage.py elections

clean_pycs:
	@find . -name "*.pyc" -delete


.PHONY: initial_data clean_pycs setup run
