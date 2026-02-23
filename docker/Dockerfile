FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências de build
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração
COPY pyproject.toml ./
COPY requirements.txt ./

# Instalar dependências e buildar wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Buildar o pacote como wheel
RUN python -m build --wheel --outdir /tmp/wheels

# Estágio final - runtime
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências mínimas
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar wheel
COPY --from=builder /tmp/wheels/*.whl ./
RUN pip install --no-cache-dir *.whl

# Copiar código da aplicação
COPY app/ ./app/

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
