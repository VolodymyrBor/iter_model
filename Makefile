test-itself:
	poetry run pytest ./tests -vv ./tests ./iter_model --flake8 --mypy \
	--cov ./iter_model --cov-branch --cov-fail-under=100

test-cov:
	poetry run pytest --cov ./iter_model --cov-report html:.cov_html \
	--cov-report term ./tests/ -vv ./tests ./iter_model --cov-branch --flake8 --mypy
