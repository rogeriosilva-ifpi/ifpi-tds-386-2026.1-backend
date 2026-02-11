# Atividade Prática: CRUD Completo de Cidades com FastAPI

**Objetivo:** Evoluir o código iniciado em aula para uma API funcional, aplicando tratamento de erros, geração automática de IDs e padrões de rotas REST.

---

## 📚 Fontes de Estudo Obrigatórias
Para realizar esta atividade, sigam as orientações do:
* **Documentação Oficial:** [FastAPI - First Steps](https://fastapi.tiangolo.com/)
* **YouTube:** [Canal Professor Rogério (/rogerio410)](https://youtube.com/rogerio410)

---

## 🛠 1. Requisitos da Atividade

### A. Geração de ID Automático
Não permitam que o usuário envie o `id` no corpo do POST. Implementem uma lógica sequencial simples:
1. Criem uma variável global: `id_atual = 4` (já que temos 4 itens na lista).
2. No momento do cadastro, incrementem essa variável e atribuam o novo valor ao campo `id` do dicionário.

### B. Expansão de Atributos
As cidades agora devem ter mais informações. Ao cadastrar ou atualizar, utilizem:
* `id` (inteiro, automático)
* `nome` (string)
* `uf` (string)
* `populacao` (inteiro)
* `ponto_turistico` (string)

### C. Implementação dos Endpoints (CRUD)
Vocês devem completar e/ou criar as seguintes rotas:

1.  **POST `/cidades`**: 
    * Recebe os dados via **Body**.
    * Gera o ID automático.
    * Retorna obrigatoriamente o **Status Code 201**.
2.  **GET `/cidades`**: 
    * Deve aceitar um **Query Param** opcional chamado `uf`. Se enviado, a API deve filtrar as cidades daquele estado.
3.  **GET `/cidades/{id}`**: 
    * Busca via **Path Param**.
    * **Tratamento de Erro:** Caso o ID não exista, deve lançar uma `HTTPException` com status **404 Not Found**.
4.  **PUT `/cidades/{id}`**: 
    * Localiza a cidade e atualiza seus campos via **Body**.
    * Lança **404** se o ID não for encontrado.
5.  **DELETE `/cidades/{id}`**: 
    * Remove a cidade da lista.
    * Lança **404** se o ID não for encontrado.

---

## 🚀 2. Desafio Master: Subrecursos e Relacionamentos

As APIs profissionais utilizam hierarquias. Pesquisem sobre **Subrecursos** e implementem o seguinte:

1.  Crie uma lista de estados: `estados_list = [{"id": 1, "nome": "Piauí", "sigla": "PI"}]`.
2.  Crie uma rota que liste todas as cidades de um estado específico usando o padrão de URL:
    * `GET /estados/{sigla}/cidades`
    * *Dica de pesquisa:* Padrão de design de URLs para recursos relacionados.

---

## 📝 Check-list de Avaliação
* [ ] O código roda sem erros?
* [ ] O `HTTPException` (404) é disparado quando busco um ID inexistente?
* [ ] O `POST` retorna Status 201?
* [ ] O ID está sendo gerado de forma sequencial (5, 6, 7...)?
* [ ] Usei Query Params para filtrar a lista?