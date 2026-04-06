.PHONY: test test-api test-unit test-all coverage clean

# Запуск всех тестов
test-all:
	python -m pytest tests/ -v --tb=short

# Только API тесты
test-api:
	python tests/test_app.py

# Только unit-тесты
test-unit:
	python -m pytest tests/test_models_unit.py tests/test_routes_unit.py -v

# Тесты с покрытием
coverage:
	python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Очистка кэша
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage

# Быстрый тест
quick:
	python -m pytest tests/test_models_unit.py -v --tb=line

# CI/CD цели
ci-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov pytest-flask

ci-test:
	pytest tests/ -v --cov=app --cov-report=xml --cov-report=term --ignore=tests/test_app.py

ci-coverage:
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing --ignore=tests/test_app.py

pre-commit:
	pre-commit run --all-files

security:
	bandit -r app/ -ll
	safety check

full-check: pre-commit security ci-test
	@echo "✅ All checks passed!"
