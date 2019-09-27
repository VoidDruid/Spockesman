CODE = spockesman
PYTHONPATH = PYTHONPATH=./:$(CODE)
INVOKE_PYTEST = $(PYTHONPATH) pytest
TEST =  $(INVOKE_PYTEST) --verbosity=2 --showlocals --strict

.PHONY: test test-fast test-failed test-cov teamcity lint format check

basetest:
	$(TEST)

test:
	$(TEST) --cov

test-fast:
	$(TEST) --exitfirst

test-failed:
	$(TEST) --last-failed

test-cov:
	$(TEST) --cov --cov-report html

lint:
	pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	black --line-length=100 --skip-string-normalization --check $(CODE)
	mypy $(CODE)
	$(INVOKE_PYTEST) --dead-fixtures --dup-fixtures

format:
	isort --apply --recursive $(CODE)
	black --line-length=100 --skip-string-normalization $(CODE)
	unify --in-place --recursive $(CODE)

validate: lint test

teamcity: export TEAMCITY_VERSION=1
teamcity: lint basetest
