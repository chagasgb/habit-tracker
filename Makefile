.PHONY: help install build test lint format clean docker-build docker-run

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências
	python -m pip install --upgrade pip
	pip install -e .[dev]

build: ## Builda o pacote como wheel
	python -m build

test: ## Executa testes
	pytest tests/ -v

test-watch: ## Executa testes em modo watch
	pytest-watch tests/ -v

lint: ## Executa linting
	black --check app/ tests/
	isort --check-only app/ tests/
	flake8 app/ tests/

format: ## Formata código
	black app/ tests/
	isort app/ tests/

clean: ## Limpa arquivos temporários
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build: ## Builda imagem Docker
	docker build -t habit-tracker:latest -f docker/Dockerfile .

docker-run: ## Executa container Docker
	docker run -p 8000:8000 habit-tracker:latest

docker-compose-up: ## Executa com docker-compose
	cd docker && docker-compose up --build

docker-compose-down: ## Para docker-compose
	cd docker && docker-compose down

dev: ## Executa em modo desenvolvimento
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

security: ## Executa verificações de segurança
	safety check
	bandit -r app/

all-checks: lint test security ## Executa todas as verificações

ci: install lint test ## Executa pipeline CI local
