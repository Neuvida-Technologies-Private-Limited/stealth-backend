# Makefile for Django Project

# Variables
PYTHON = python
MANAGE_PY = manage.py

# Targets and Commands
runserver:
	$(PYTHON) $(MANAGE_PY) runserver

migrate:
	$(PYTHON) $(MANAGE_PY) migrate

createsuperuser:
	$(PYTHON) $(MANAGE_PY) createsuperuser

# You can add more targets for your specific use cases here
