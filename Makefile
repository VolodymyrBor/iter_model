
run_ruff:
	poetry run ruff check ./tests ./iter_model


run_mypy:
	poetry run mypy ./tests ./iter_model


run_tests:
	poetry run pytest ./tests -vv ./tests ./iter_model \
	--cov ./iter_model --cov-branch --cov-fail-under=100


run_linters_and_tests: run_ruff run_mypy run_tests
