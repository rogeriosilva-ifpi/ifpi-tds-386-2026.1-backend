# Projeto de Referência Didático
## Backend com FastAPI usando Clean Architecture + DDD

## Objetivo

Criar um **projeto de referência didático** para ensino de **Backend em Python com FastAPI**, demonstrando na prática:

- Clean Architecture
- Domain Driven Design (DDD)
- Princípios SOLID
- Separação clara de responsabilidades
- Padrão Repository
- Uso de Pydantic
- Uso de SQLModel
- Sistema de migrations
- Uso de `.env` para configuração
- Organização didática de código para ensino

O projeto será utilizado em uma **disciplina de Backend** e deve ser **claramente estruturado e comentado** para facilitar aprendizado.

---

# Contexto da Aplicação

A aplicação será um **CRUD de Gestão de Eventos Acadêmicos**.

Exemplos de eventos:

- Congressos
- Seminários
- Workshops
- Palestras
- Minicursos

Funcionalidades principais:

- Cadastro de eventos
- Listagem de eventos
- Atualização de eventos
- Remoção de eventos
- Consulta por período
- Consulta por tipo de evento

Campos sugeridos para Evento:

- id
- title
- description
- event_type
- start_date
- end_date
- location
- organizer
- created_at
- updated_at

---

# Tecnologias Obrigatórias

- Python 3.11+
- FastAPI
- Pydantic
- SQLModel
- Alembic (migrations)
- PostgreSQL (preferencial), mas compatível com SQLite e MySQL
- python-dotenv ou pydantic-settings para `.env`

---

# Objetivos Arquiteturais

O projeto deve demonstrar claramente:

## Clean Architecture

Separação em camadas:

- **Presentation**
- **Application**
- **Domain**
- **Infrastructure**

Dependências devem seguir a regra:
presentation -> application -> domain
infrastructure -> domain


Ou seja:

- Camadas externas dependem das internas
- Domain não depende de ninguém

---

# Princípios SOLID a demonstrar

Principalmente:

### SRP — Single Responsibility Principle

Cada classe deve ter **uma única responsabilidade clara**.

### DIP — Dependency Inversion Principle

- Camadas superiores dependem de **abstrações**
- Implementações concretas ficam na infraestrutura

### OCP — Open Closed Principle

A arquitetura deve permitir **extensão sem modificação**.

---

# Estrutura de Pastas Esperada

O projeto deve ser gerado com estrutura clara e didática.

academic-events-api/

app/
presentation/
    api/
        routes/
            event_routes.py
        controllers/
            event_controller.py
    schemas/
        event_view_models.py

application/
    services/
        event_service.py
    dto/
        event_dto.py

domain/
    entities/
        event_entity.py
    repositories/
        event_repository.py
    value_objects/
        event_type.py

infrastructure/
    database/
        db.py
        models/
            event_model.py
    repositories/
        event_repository_sqlmodel.py
    config/
        settings.py

shared/
    dependencies.py

alembic/

tests/

main.py

.env.example


Cada pasta deve conter **comentários explicativos**.

---

# Descrição das Camadas

## Domain

Contém **regras de negócio puras**.

Não deve depender de:

- FastAPI
- SQLModel
- banco de dados
- frameworks

Deve conter:

### Entities

Representação conceitual da entidade.

Exemplo: EventRepository


Métodos esperados:

- create
- get_by_id
- list
- update
- delete

---

## Application

Contém **casos de uso da aplicação**.

Exemplo:

EventService


Responsabilidades:

- coordenar regras de negócio
- usar interfaces de repositório
- aplicar validações de negócio

Não deve conhecer:

- SQL
- FastAPI
- infraestrutura

---

## Infrastructure

Contém **implementações concretas**.

Inclui:

- banco de dados
- SQLModel
- implementações de repositórios

Exemplo: EventRepositorySQLModel

Implementa: EventRepository


---

## Presentation

Contém:

- rotas FastAPI
- controllers
- view models

Separação clara entre:
routes
controllers
schemas


Fluxo esperado:

Request
↓
Route
↓
Controller
↓
Application Service
↓
Repository (interface)
↓
Infrastructure Repository
↓
Database


---

# Uso de Models

Podem existir **dois tipos de models**:

### 1 — ViewModels (Pydantic)

Usados para:

- requests
- responses

Local:
presentation/schemas


### 2 — Database Models (SQLModel)

Usados para:

- persistência

Local:
infrastructure/database/models


---

# Banco de Dados

Utilizar **SQLModel**.

Suportar:

- PostgreSQL
- MySQL
- SQLite

Configuração via `.env`.

---

# Sistema de Configuração

Implementar configuração baseada em `.env`.

Exemplo:
DATABASE_URL=
APP_ENV=
DEBUG=


Arquivo:
infrastructure/config/settings.py


Usar:
pydantic-settings ou python-dotenv


---

# Sistema de Migrations

Implementar migrations usando:
Alembic


Configurar para funcionar com SQLModel.

Criar exemplo de migration inicial:

create_event_table


---

# Dependency Injection

Utilizar **injeção de dependências do FastAPI**.

Arquivo sugerido:

shared/dependencies.py


Exemplo:

- provider de database session
- provider de repositories
- provider de services

---

# API Endpoints Esperados

Prefixo:
/events
Endpoints:

### Criar evento


POST /events


### Listar eventos


GET /events


### Buscar evento


GET /events/{id}


### Atualizar evento


PUT /events/{id}


### Remover evento


DELETE /events/{id}


### Buscar por período


GET /events?start_date=&end_date=


---

# Arquivo main.py

Deve:

- criar app FastAPI
- registrar rotas
- carregar configurações
- iniciar infraestrutura

---

# Banco padrão para execução simples

Utilizar:


SQLite


Por padrão, mas permitir alterar para PostgreSQL via `.env`.

---

# Testes

Criar exemplos simples usando:


pytest


Testes de:

- service
- repository

---

# Requisitos Didáticos

O projeto deve ser **altamente didático**.

Incluir:

- comentários explicativos
- docstrings
- explicação de decisões arquiteturais

Exemplo:

Este service implementa o caso de uso de criação de eventos.
Ele depende apenas da interface EventRepository, respeitando DIP.


---

# README.md Final

Ao final, gerar um **README.md detalhado explicando**:

1. Arquitetura usada
2. Estrutura de pastas
3. Fluxo de requisição
4. Onde cada responsabilidade está
5. Como rodar o projeto
6. Como rodar migrations
7. Como rodar testes

Explicar também:

- Clean Architecture
- DDD
- SOLID aplicados no projeto

---

# Qualidade Esperada

O código deve ser:

- claro
- modular
- organizado
- fortemente tipado
- consistente com boas práticas de Python

Este projeto será utilizado como **material de ensino em disciplina de Backend com FastAPI**.