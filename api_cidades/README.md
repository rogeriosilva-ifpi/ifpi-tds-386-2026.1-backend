# 🌆 API de Cidades - FastAPI

## 📋 Sobre o Projeto

Esta é uma API REST simples desenvolvida com **FastAPI** para gerenciamento de cidades. O projeto demonstra os conceitos fundamentais de desenvolvimento de APIs RESTful, incluindo operações CRUD (Create, Read, Update, Delete).

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.7 ou superior instalado
- pip (gerenciador de pacotes do Python)

### Passo 1: Criar e Ativar o Ambiente Virtual

#### 🪟 Windows
```bash
# Criar ambiente virtual
python -m venv .env

# Ativar ambiente virtual
.env\Scripts\activate
```

#### 🐧 Linux/Mac
```bash
# Criar ambiente virtual
python3 -m venv .env

# Ativar ambiente virtual
source .env/bin/activate
```

### Passo 2: Instalar Dependências
```bash
pip install fastapi
```

### Passo 3: Executar o Servidor
```bash
# Modo desenvolvimento (com auto-reload)
fastapi dev main.py

# OU modo produção
fastapi run main.py
```

### Passo 4: Acessar a API
- **API**: http://localhost:8000
- **Documentação Interativa (Swagger)**: http://localhost:8000/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8000/redoc

---

## 📖 Explicação do Código

### Estrutura Básica

```python
from fastapi import FastAPI

app = FastAPI()
```
- Importa o framework FastAPI
- Cria uma instância da aplicação

### Banco de Dados Simulado

```python
cidades_list = [
  {'id': 1, 'nome': 'Teresina', 'uf': 'PI'},
  {'id': 2, 'nome': 'Altos', 'uf': 'PI'},
  {'id': 3, 'nome': 'Coelho Neto', 'uf': 'MA'},
  {'id': 4, 'nome': 'Pedro II', 'uf': 'PI'},
]
```
- Lista Python simulando um banco de dados
- Cada cidade é um dicionário com `id`, `nome` e `uf`

### Endpoints Implementados

#### 1. Listar Todas as Cidades
```python
@app.get('/cidades')
def listar_cidades():
  return cidades_list
```
- **Método**: GET
- **Rota**: `/cidades`
- **Função**: Retorna todas as cidades cadastradas
- **Exemplo de uso**: http://localhost:8000/cidades

#### 2. Buscar Cidade por ID
```python
@app.get('/cidades/{id}')
def detalhes_cidade(id: int):
  for cidade in cidades_list:
    if cidade['id'] == id:
      return cidade
```
- **Método**: GET
- **Rota**: `/cidades/{id}`
- **Parâmetro**: `id` (inteiro na URL)
- **Função**: Retorna os detalhes de uma cidade específica
- **Exemplo de uso**: http://localhost:8000/cidades/1

#### 3. Remover Cidade
```python
@app.delete('/cidade/{id}')
def remover_cidade(id: int):
  for index, cidade in enumerate(cidades_list):
    if cidade['id'] == id:
      cidades_list.pop(index)
      return
```
- **Método**: DELETE
- **Rota**: `/cidade/{id}`
- **Parâmetro**: `id` (inteiro na URL)
- **Função**: Remove uma cidade da lista
- **Nota**: ⚠️ Endpoint possui inconsistência na rota (singular vs plural)

---

## 🌐 O que é uma API REST?

**REST** (Representational State Transfer) é um estilo arquitetural para desenvolvimento de APIs web que utiliza o protocolo HTTP.

### Princípios Básicos do REST:
- **Cliente-Servidor**: Separação entre interface e armazenamento de dados
- **Stateless**: Cada requisição é independente
- **Interface Uniforme**: Uso padronizado de URLs e métodos HTTP
- **Recursos**: Entidades manipuladas pela API (ex: cidades)

---

## 🔧 Métodos HTTP (Verbos)

| Método | Descrição | Uso Comum | Idempotente |
|--------|-----------|-----------|-------------|
| **GET** | Recupera dados | Listar ou buscar recursos | ✅ Sim |
| **POST** | Cria novos recursos | Adicionar novo item | ❌ Não |
| **PUT** | Atualiza recurso completo | Substituir item existente | ✅ Sim |
| **PATCH** | Atualiza parcialmente | Modificar campos específicos | ❌ Não |
| **DELETE** | Remove recursos | Excluir item | ✅ Sim |

### Exemplos neste projeto:
- `GET /cidades` → Lista todas as cidades
- `GET /cidades/1` → Busca a cidade com ID 1
- `DELETE /cidade/1` → Remove a cidade com ID 1

---

## 📊 HTTP Status Codes (Códigos de Estado)

### Status Codes Mais Comuns:

#### 2xx - Sucesso
- **200 OK**: Requisição bem-sucedida (GET, PUT, PATCH)
- **201 Created**: Recurso criado com sucesso (POST)
- **204 No Content**: Sucesso sem conteúdo de retorno (DELETE)

#### 4xx - Erros do Cliente
- **400 Bad Request**: Dados inválidos na requisição
- **404 Not Found**: Recurso não encontrado
- **422 Unprocessable Entity**: Validação falhou

#### 5xx - Erros do Servidor
- **500 Internal Server Error**: Erro interno no servidor

### ⚠️ Melhorias Necessárias neste Código:
```python
# Código atual - não retorna 404 quando cidade não existe
@app.get('/cidades/{id}')
def detalhes_cidade(id: int):
  for cidade in cidades_list:
    if cidade['id'] == id:
      return cidade
  # ❌ Não trata o caso de não encontrar
```

**Melhor prática:**
```python
from fastapi import HTTPException

@app.get('/cidades/{id}')
def detalhes_cidade(id: int):
  for cidade in cidades_list:
    if cidade['id'] == id:
      return cidade
  raise HTTPException(status_code=404, detail="Cidade não encontrada")
```

---

## 📝 Convenções de Código REST

### 1. Nomenclatura de Rotas (URLs)
✅ **Boas Práticas:**
- Use substantivos no plural: `/cidades`, `/usuarios`
- Use minúsculas: `/cidades` (não `/Cidades`)
- Use hífen para separar palavras: `/cidades-brasileiras`
- Seja consistente: sempre plural OU sempre singular

❌ **Problema neste código:**
```python
@app.get('/cidades')      # ✅ Plural
@app.get('/cidades/{id}')  # ✅ Plural
@app.delete('/cidade/{id}') # ❌ Singular - inconsistente!
```

### 2. Estrutura de Rotas RESTful

| Operação | Método | Rota | Descrição |
|----------|--------|------|-----------|
| Listar todos | GET | `/cidades` | Lista todas as cidades |
| Buscar um | GET | `/cidades/{id}` | Busca cidade específica |
| Criar | POST | `/cidades` | Cria nova cidade |
| Atualizar completo | PUT | `/cidades/{id}` | Atualiza cidade completa |
| Atualizar parcial | PATCH | `/cidades/{id}` | Atualiza campos específicos |
| Deletar | DELETE | `/cidades/{id}` | Remove cidade |

### 3. Formato de Resposta
- Use JSON como formato padrão
- Retorne objetos consistentes
- Inclua metadados quando necessário

```json
{
  "data": [...],
  "total": 4,
  "page": 1
}
```

---

## 📚 Documentação Automática do FastAPI

Uma das grandes vantagens do **FastAPI** é a geração automática de documentação interativa!

### 🔍 Swagger UI - `/docs`
Acesse: **http://localhost:8000/docs**

Recursos:
- Interface visual interativa
- Testar endpoints diretamente no navegador
- Ver parâmetros, tipos de dados e respostas
- Executar requisições sem ferramentas externas

### 📖 ReDoc - `/redoc`
Acesse: **http://localhost:8000/redoc**

Recursos:
- Documentação estilo artigo
- Layout mais limpo e organizado
- Ideal para leitura e referência

### Como Melhorar a Documentação:

```python
@app.get('/cidades',
         summary="Lista todas as cidades",
         description="Retorna uma lista com todas as cidades cadastradas no sistema",
         response_description="Lista de cidades")
def listar_cidades():
  return cidades_list
```

---

## 🔄 Testando a API

### Usando o Navegador (apenas GET):
```
http://localhost:8000/cidades
http://localhost:8000/cidades/1
```

### Usando curl (terminal):

```bash
# Listar cidades
curl http://localhost:8000/cidades

# Buscar cidade específica
curl http://localhost:8000/cidades/1

# Deletar cidade
curl -X DELETE http://localhost:8000/cidade/1
```

### Usando a Documentação Interativa:
1. Acesse http://localhost:8000/docs
2. Clique no endpoint desejado
3. Clique em "Try it out"
4. Preencha os parâmetros (se necessário)
5. Clique em "Execute"

---

## 🎯 Próximos Passos e Melhorias

1. **Adicionar método POST** para criar novas cidades
2. **Adicionar método PUT/PATCH** para atualizar cidades
3. **Implementar tratamento de erros** (HTTPException)
4. **Corrigir inconsistência** na rota DELETE (`/cidade` → `/cidades`)
5. **Adicionar validação de dados** com Pydantic models
6. **Conectar a um banco de dados** real (SQLite, PostgreSQL)
7. **Implementar autenticação e autorização**

---

## 📚 Recursos de Aprendizado

- [Documentação Oficial do FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial Completo FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [HTTP Status Codes](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status)
- [REST API Best Practices](https://restfulapi.net/)

---

**Desenvolvido para fins educacionais - IFPI TDS 2026.1**
