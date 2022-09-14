.PHONY: test coverage


test:
	@python3 -m pytest tests \
	--junitxml=tests-result.xml \
	--html=dist/reports/html/tests-result.html

coverage:
	@python3 -m pytest tests \
	--junitxml=tests-result.xml \
	--html=dist/reports/html/tests-result.html \
	--cov-report term \
	--cov-branch \
	--cov=. \
	&& coverage xml -o coverage.xml \
	&& coverage html -d dist/reports/html/coverage_html
