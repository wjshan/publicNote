.ONESHELL:
ENV_PREFIX=""

serve:
	$(ENV_PREFIX)mkdocs serve

install:
	$(ENV_PREFIX)pip install -e .[dev]

github_install:
	$(ENV_PREFIX)pip install -e .

build:
	$(ENV_PREFIX)mkdocs build

build_docker:
	docker-compose -f docker-compose.yml up && docker-compose -f docker-compose.yml down