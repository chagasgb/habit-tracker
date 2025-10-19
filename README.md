# 🎯 Habit Tracker API

API para rastreamento de hábitos desenvolvida com FastAPI, SQLAlchemy e MySQL.

## 🚀 Características

- ✅ API RESTful com FastAPI
- 🗄️ Banco de dados MySQL com SQLAlchemy
- 🧪 Testes automatizados com pytest
- 🐳 Containerização com Docker
- 🔄 CI/CD com GitHub Actions
- 📦 Build com wheels para distribuição
- 🔒 Verificações de segurança automatizadas

## 📋 Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Git

## 🛠️ Instalação e Desenvolvimento

### Usando Make (Recomendado)

```bash
# Instalar dependências
make install

# Executar testes
make test

# Executar em modo desenvolvimento
make dev

# Executar todas as verificações (lint, test, security)
make all-checks

# Ver todos os comandos disponíveis
make help
```

### Instalação Manual

```bash
# Clonar repositório
git clone <seu-repositorio>
cd habit-tracker

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -e .[dev]

# Executar testes
pytest tests/ -v

# Executar aplicação
uvicorn app.main:app --reload
```

## 🐳 Docker

### Build e execução

```bash
# Build da imagem
make docker-build

# Executar container
make docker-run

# Ou usar docker-compose (com MySQL)
make docker-compose-up
```

### Acessar a aplicação

- API: http://localhost:8000
- Documentação: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🧪 Testes

```bash
# Executar todos os testes
make test

# Executar com coverage
pytest tests/ --cov=app --cov-report=html

# Executar testes específicos
pytest tests/test_habits.py -v

# Executar em modo watch
make test-watch
```

## 🔄 CI/CD

O projeto inclui um pipeline completo do GitHub Actions que:

1. **Testes**: Executa testes em Python 3.10, 3.11 e 3.12
2. **Linting**: Verifica formatação com Black e Isort
3. **Segurança**: Executa verificações com Safety e Bandit
4. **Build**: Constrói e testa o pacote wheel
5. **Docker**: Builda e publica imagem Docker
6. **Coverage**: Gera relatórios de cobertura

### Secrets necessários no GitHub

```bash
DOCKER_USERNAME=seu_usuario_dockerhub
DOCKER_PASSWORD=seu_token_dockerhub
```

## 📦 Build do Pacote

```bash
# Buildar wheel
make build

# Instalar wheel localmente
pip install dist/*.whl

# Instalar com dependências de desenvolvimento
pip install dist/*.whl[dev]
```

## 🔒 Verificações de Segurança

```bash
# Executar verificações de segurança
make security

# Verificar vulnerabilidades
safety check

# Análise estática de segurança
bandit -r app/
```

## 📊 Estrutura do Projeto

```
habit-tracker/
├── app/                    # Código da aplicação
│   ├── core/              # Configurações principais
│   ├── models/            # Modelos SQLAlchemy
│   ├── routes/            # Rotas da API
│   ├── schemas/           # Schemas Pydantic
│   ├── services/          # Lógica de negócio
│   └── main.py           # Aplicação principal
├── tests/                 # Testes automatizados
├── .github/workflows/     # GitHub Actions
├── pyproject.toml        # Configuração do projeto
├── Dockerfile            # Imagem Docker
├── docker-compose.yml    # Orquestração de containers
├── Makefile             # Comandos de desenvolvimento
└── README.md            # Este arquivo
```

## 🎯 Endpoints da API

- `GET /health` - Health check
- `GET /habits` - Listar hábitos
- `POST /habits` - Criar hábito
- `DELETE /habits/{id}` - Excluir hábito
- `GET /records` - Listar registros
- `POST /records` - Criar registro

Documentação completa disponível em: http://localhost:8000/docs

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique os [Issues](../../issues) existentes
2. Crie um novo issue se necessário
3. Entre em contato: gabriel@example.com
