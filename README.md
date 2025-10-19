# 🎯 Habit Tracker API

[![CI - Build and Test](https://github.com/chagasgb/habit-tracker/workflows/CI%20-%20Build%20and%20Test/badge.svg)](https://github.com/chagasgb/habit-tracker/actions)

API simples para rastreamento de hábitos desenvolvida com FastAPI, SQLAlchemy e MySQL.

## 📋 Sobre o Projeto

Esta API permite gerenciar hábitos e seus registros de execução. Você pode criar hábitos, definir suas frequências e registrar quando foram realizados.

### Principais funcionalidades:
- ✅ Criar e gerenciar hábitos
- 📊 Registrar execuções dos hábitos
- 🔄 API RESTful com documentação automática
- 🗄️ Persistência em banco de dados MySQL
- 🧪 Testes automatizados

## 🚀 Como usar

### Instalação rápida

```bash
# Clonar o projeto
git clone <seu-repositorio>
cd habit-tracker

# Instalar dependências
make install

# Executar aplicação
make dev
```

### Com Docker

```bash
# Executar com docker-compose (inclui MySQL)
make docker-compose-up
```

### Acessar a API

- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 Testes

```bash
# Executar testes
make test

# Ver todos os comandos disponíveis
make help
```

## 📦 Build

O projeto é distribuído como wheel e inclui CI/CD automatizado:

```bash
# Build local
make build
```

## 🎯 Endpoints principais

- `GET /habits` - Listar hábitos
- `POST /habits` - Criar hábito
- `DELETE /habits/{id}` - Excluir hábito
- `GET /records` - Listar registros
- `POST /records` - Criar registro

