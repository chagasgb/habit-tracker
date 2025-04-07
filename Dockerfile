FROM python:3.11

WORKDIR /app

# Copia o requirements.txt primeiro (boa prática: aproveita cache)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
#COPY . app

# Inicia o FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
