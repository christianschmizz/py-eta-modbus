.PHONY: test
test:
	@pytest --verbose

.PHONY: ci
ci:
	@pytest tests --junitxml=report.xml

.PHONY: coverage
coverage:
	@pytest --cov-config .coveragerc --cov-report term --cov-report xml --cov=oasis --verbose tests/

# flake is configured in setup.cfg
.PHONY: flake
flake8:
	@flake8 --exclude oasis/hzd oasis

.PHONY: build
build:
	@python3 -m pip install --upgrade build
	@python3 -m build

.PHONY: dist
dist:
	python3 -m pip install --upgrade twine
