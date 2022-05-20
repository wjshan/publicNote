.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

serve:
	$(ENV_PREFIX)mkdocs serve

install:
	$(ENV_PREFIX)pip install -e .[dev]

github_install:
	$(ENV_PREFIX)pip install -e .

build:
	$(ENV_PREFIX)mkdocs build