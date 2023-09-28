.PHONY: test

flask:
	@poetry run python -m flask --app metastock/http.py run

test:
	@poetry run python -m pytest

queue-analysis-job:
	@ENVIRONMENT=development poetry run python -m metastock queue:consumer:start stock_trading_analysis_job_consumer

prod-queue-analysis-job:
	@ENVIRONMENT=production poetry run python -m metastock queue:consumer:start stock_trading_analysis_job_consumer