# Usar imagem oficial Python slim
FROM python:3.11-slim

WORKDIR /cli

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar o código do CLI
COPY . .

# Definir entrypoint para o CLI
ENTRYPOINT ["python3"]
