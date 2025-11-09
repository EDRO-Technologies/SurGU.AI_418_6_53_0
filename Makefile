.PHONY: lint-backend format-backend type-check-backend check-backend
.PHONY: docker-dev docker-prod docker-build docker-down docker-logs
.PHONY: clean

BACKEND_DIR := backend
FRONTEND_DIR := frontend
PYPROJECT_TOML := $(BACKEND_DIR)/pyproject.toml
UV_LOCK := $(BACKEND_DIR)/uv.lock

lint-backend:
	@echo "Running ruff linter (config: $(PYPROJECT_TOML))..."
	cd $(BACKEND_DIR) && uv run ruff check .

lint-backend-fix:
	@echo "Running ruff linter with autofix (config: $(PYPROJECT_TOML))..."
	cd $(BACKEND_DIR) && uv run ruff check . --fix --unsafe-fixes

format-backend:
	@echo "Formatting code (config: $(PYPROJECT_TOML))..."
	cd $(BACKEND_DIR) && uv run ruff format .

format-backend-check:
	@echo "Checking code format (config: $(PYPROJECT_TOML))..."
	cd $(BACKEND_DIR) && uv run ruff format . --check

type-check-backend:
	@echo "Running type checker (config: $(PYPROJECT_TOML))..."
	cd $(BACKEND_DIR) && uv run pyright

check-backend: lint-backend-fix format-backend type-check-backend

pre-commit-backend:
	@echo "Running pre-commit hooks..."
	cd $(BACKEND_DIR) && uv run pre-commit run --all-files

docker-dev: docker-dev-build docker-logs

docker-prod: docker-prod-build docker-logs

docker-dev-build:
	docker compose --profile dev up --build

docker-prod-build:
	docker compose --profile prod up -d --build

docker-down:
	docker compose --profile dev --profile prod down

docker-logs:
	docker compose logs -f

clean:
	@echo "Cleaning cache and temp files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pyright" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	@echo "[OK] Cleanup completed"
