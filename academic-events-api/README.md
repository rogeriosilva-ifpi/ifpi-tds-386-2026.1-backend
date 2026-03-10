# Academic Events API

Projeto didático de **Backend com FastAPI** demonstrando na prática:
**Clean Architecture + DDD + SOLID + Repository Pattern**

> **Disciplina:** Programação Web Backend — IFPI TDS
> **Professor:** Rogério | **Ano:** 2026.1

---

## Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Arquitetura](#arquitetura)
3. [Estrutura de Pastas](#estrutura-de-pastas)
4. [Fluxo de uma Requisição](#fluxo-de-uma-requisição)
5. [SOLID na Prática](#solid-na-prática)
6. [Como Rodar](#como-rodar)
7. [Endpoints da API](#endpoints-da-api)
8. [Migrations com Alembic](#migrations-com-alembic)
9. [Testes](#testes)
10. [Marcos do Projeto](#marcos-do-projeto)

---

## Sobre o Projeto

API REST para **Gestão de Eventos Acadêmicos** (congressos, seminários, workshops, etc.).

O objetivo **não é só fazer funcionar** — é demonstrar como organizar um projeto backend profissional, separando claramente as responsabilidades de cada parte do código.

---

## Arquitetura

### Clean Architecture

O projeto segue o modelo de camadas concêntricas onde **as dependências sempre apontam para dentro**:

```
┌─────────────────────────────────────┐
│           Presentation              │  ← HTTP, FastAPI, JSON
│  ┌───────────────────────────────┐  │
│  │        Application            │  │  ← Casos de uso
│  │  ┌─────────────────────────┐  │  │
│  │  │        Domain           │  │  │  ← Regras de negócio (puro Python)
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
         Infrastructure               ← Banco, ORM, frameworks
              ↓
           Domain (interface)
```

**Regra fundamental:** camadas externas conhecem as internas, **nunca o contrário**.

| Camada | Conhece | Não conhece |
|--------|---------|-------------|
| Domain | — (nada) | FastAPI, SQLModel, banco |
| Application | Domain | FastAPI, SQL, HTTP |
| Infrastructure | Domain | Application, Presentation |
| Presentation | Application | SQL, banco |

### DDD — Domain Driven Design

O código reflete a linguagem do negócio:

- **Entity** (`Event`): objeto com identidade única, contém regras de negócio
- **Value Object** (`EventType`): definido por seus valores, sem identidade
- **Repository** (`EventRepository`): abstração de coleção de entidades
- **Service** (`EventService`): orquestra casos de uso complexos

---

## Estrutura de Pastas

```
academic-events-api/
│
├── main.py                         # Ponto de entrada — registra rotas, inicializa DB
│
├── app/
│   │
│   ├── domain/                     # NÚCLEO — Python puro, zero dependências externas
│   │   ├── entities/
│   │   │   └── event_entity.py     # Entidade Event com regras de negócio
│   │   ├── repositories/
│   │   │   └── event_repository.py # Interface (ABC) do repositório
│   │   └── value_objects/
│   │       └── event_type.py       # Enum de tipos de eventos
│   │
│   ├── application/                # CASOS DE USO — orquestra domain + infra
│   │   ├── dto/
│   │   │   └── event_dto.py        # CreateEventDTO, UpdateEventDTO
│   │   └── services/
│   │       └── event_service.py    # 5 casos de uso: create, list, get, update, delete
│   │
│   ├── infrastructure/             # IMPLEMENTAÇÕES CONCRETAS
│   │   ├── config/
│   │   │   └── settings.py         # Configurações via .env (pydantic-settings)
│   │   ├── database/
│   │   │   ├── db.py               # Engine, Session, create_db_and_tables()
│   │   │   └── models/
│   │   │       └── event_model.py  # Tabela 'events' (SQLModel ORM)
│   │   └── repositories/
│   │       └── event_repository_sqlmodel.py  # Implementa EventRepository com SQL
│   │
│   ├── presentation/               # FRONTEIRA HTTP
│   │   ├── schemas/
│   │   │   └── event_view_models.py  # Request/Response schemas (Pydantic)
│   │   └── api/
│   │       ├── controllers/
│   │       │   └── event_controller.py  # Converte HTTP ↔ Application
│   │       └── routes/
│   │           └── event_routes.py      # Define URLs e métodos HTTP
│   │
│   └── shared/
│       └── dependencies.py         # Fio condutor: wiring de todas as dependências
│
├── alembic/                        # Migrations do banco de dados
│   ├── env.py
│   └── versions/
│       └── 562c2c6193ba_create_events_table.py
│
├── tests/
│   ├── conftest.py                 # Fixtures: banco em memória, client, service
│   ├── test_event_service.py       # 14 testes da camada Application
│   └── test_event_api.py           # 13 testes de integração da API HTTP
│
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## Fluxo de uma Requisição

Exemplo: `POST /events` para criar um evento.

```
1. Cliente envia JSON via HTTP
        ↓
2. event_routes.py
   Define: POST /events, status 201, response_model=EventResponse
        ↓
3. EventController.create()
   Converte: EventCreateRequest (ViewModel) → CreateEventDTO
        ↓
4. EventService.create_event()
   - Cria a entidade Event (domain)
   - Chama event.validate() (regras de negócio)
   - Chama repository.create(event)
        ↓
5. EventRepository (interface)
   — o service não sabe qual implementação está usando —
        ↓
6. EventRepositorySQLModel.create()
   - Converte Event → EventModel
   - session.add() + session.commit()
   - Retorna Event com ID gerado
        ↓
7. EventController
   Converte: Event (domain) → EventResponse (ViewModel)
        ↓
8. FastAPI serializa para JSON e retorna 201 Created
```

---

## SOLID na Prática

### SRP — Single Responsibility Principle

Cada classe tem **uma única razão para mudar**:

| Classe | Única responsabilidade |
|--------|----------------------|
| `Event` (entity) | Representa o conceito de Evento no domínio |
| `EventService` | Orquestra casos de uso de Eventos |
| `EventRepositorySQLModel` | Persiste Eventos no banco com SQLModel |
| `EventController` | Converte HTTP ↔ Application |
| `Settings` | Gerencia configurações da aplicação |

### DIP — Dependency Inversion Principle

`EventService` depende da **interface** `EventRepository`, não da implementação:

```python
# ✅ CORRETO — depende da abstração
class EventService:
    def __init__(self, repository: EventRepository):  # Interface!
        self._repository = repository

# ❌ ERRADO — dependeria da implementação
class EventService:
    def __init__(self):
        self._repository = EventRepositorySQLModel()  # Acoplado!
```

O wiring acontece em `shared/dependencies.py` — o único lugar onde a implementação concreta é instanciada.

### OCP — Open/Closed Principle

Para trocar o banco de dados (ex: de SQLite para MongoDB):
1. Crie `EventRepositoryMongo` implementando `EventRepository`
2. Altere `get_event_repository()` em `dependencies.py`
3. **Zero mudanças** em Domain, Application ou Presentation

---

## Como Rodar

### Pré-requisitos

- Python 3.11+

### Instalação

```bash
# Clone o repositório e entre na pasta
cd academic-events-api

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
# ou
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env se necessário (SQLite já é o padrão)
```

### Rodando o servidor

```bash
# Modo desenvolvimento (com auto-reload)
uvicorn main:app --reload

# Ou
python main.py
```

Acesse:
- **API:** http://localhost:8000
- **Swagger UI (documentação):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Endpoints da API

| Método | URL | Descrição | Status |
|--------|-----|-----------|--------|
| `GET` | `/health` | Health check | 200 |
| `POST` | `/events/` | Criar evento | 201 |
| `GET` | `/events/` | Listar eventos | 200 |
| `GET` | `/events/?start_date=&end_date=` | Filtrar por período | 200 |
| `GET` | `/events/{id}` | Buscar por ID | 200 |
| `PUT` | `/events/{id}` | Atualizar evento | 200 |
| `DELETE` | `/events/{id}` | Remover evento | 204 |

### Exemplo de criação (POST /events/)

```json
{
  "title": "I Congresso de Tecnologia do IFPI",
  "description": "Congresso sobre inovações em TI",
  "event_type": "congress",
  "start_date": "2026-08-10T08:00:00",
  "end_date": "2026-08-12T18:00:00",
  "location": "Auditório Principal - IFPI",
  "organizer": "Prof. Rogério"
}
```

**Tipos de evento válidos:** `congress`, `seminar`, `workshop`, `lecture`, `short_course`, `symposium`, `other`

---

## Migrations com Alembic

```bash
# Aplicar todas as migrations (criar tabelas)
alembic upgrade head

# Ver versão atual do banco
alembic current

# Ver histórico de migrations
alembic history

# Criar nova migration após alterar um model
alembic revision --autogenerate -m "descrição_da_mudança"

# Reverter uma versão
alembic downgrade -1
```

> **Nota:** No desenvolvimento com SQLite, o `main.py` já cria as tabelas automaticamente via `create_db_and_tables()`. Use Alembic em produção.

---

## Testes

```bash
# Rodar todos os testes
pytest

# Com detalhes de cada teste
pytest -v

# Rodar apenas testes da API
pytest tests/test_event_api.py

# Rodar apenas testes do service
pytest tests/test_event_service.py
```

### Cobertura de testes (27 testes)

| Arquivo | Testes | O que testa |
|---------|--------|-------------|
| `test_event_service.py` | 14 | Casos de uso (create, list, get, update, delete + erros) |
| `test_event_api.py` | 13 | Endpoints HTTP completos (status codes, payloads, filtros) |

---

## Marcos do Projeto

O projeto foi construído incrementalmente em 10 marcos (branches git):

| Branch | O que foi adicionado |
|--------|---------------------|
| `marco-01-estrutura-base` | Estrutura de pastas, requirements, .env.example, main.py |
| `marco-02-domain` | Entities, Repository interface, Value Objects |
| `marco-03-infrastructure-config-db` | Settings (.env), Engine, EventModel (ORM) |
| `marco-04-infrastructure-repository` | EventRepositorySQLModel (implementação) |
| `marco-05-application` | DTOs e EventService (casos de uso) |
| `marco-06-presentation` | ViewModels, Controller, Routes |
| `marco-07-dependency-injection` | dependencies.py, main.py completo |
| `marco-08-migrations` | Alembic configurado + migration inicial |
| `marco-09-testes` | 27 testes pytest (service + API) |
| `marco-10-readme` | README.md completo |

Para explorar um marco específico:
```bash
git checkout marco-03-infrastructure-config-db
```
