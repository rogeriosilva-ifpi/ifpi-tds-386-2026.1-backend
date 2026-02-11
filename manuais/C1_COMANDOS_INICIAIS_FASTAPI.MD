# 🚀 Guia de Terminal: Desenvolvimento Backend (FastAPI)
**Curso:** Técnico em Desenvolvimento de Sistemas (TDS) - IFPI
**Professor:** Rogério

Este guia explica os comandos fundamentais utilizados para configurar seu ambiente de desenvolvimento Backend.

---

## 📂 1. Navegação e Gestão de Pastas

### `mkdir` (Make Directory)
* **Comando:** `mkdir ifpi-tds-386-2026.1-backend`
* **Objetivo:** Cria uma pasta para organizar seu projeto.
* **Variação:** No Windows e Linux, o comando é o mesmo. Use `mkdir -p` (Linux) ou apenas crie pastas em sequência no Windows.

### `cd` (Change Directory)
* **Comando:** `cd ifpi-tds-386-2026.1-backend`
* **Objetivo:** Entra na pasta criada. 
* **Dica:** Digite `cd ifpi` e aperte a tecla **TAB** para o terminal completar o nome da pasta automaticamente.

### `ls` / `dir` (Listar Conteúdo)
* **Linux/Mac:** `ls -la` (Lista detalhes e arquivos ocultos).
* **Windows (CMD):** `dir`
* **Windows (PowerShell):** `ls` ou `dir` funcionam.

---

## 🐍 2. Ambiente Virtual (Virtualenv)

O ambiente virtual é essencial para não "bagunçar" o Python do seu computador com bibliotecas de diferentes projetos.

### Criando o ambiente
* **Comando:** `python -m venv .env`
* **Explicação:** O `-m venv` chama o módulo de ambiente virtual e `.env` é o nome da pasta que será criada.

### Ativando o ambiente (Diferença Crucial!)
Aqui é onde a maioria dos alunos se confunde. O comando muda conforme o sistema:

* **No Linux / Mac / Git Bash:**
  `source ./.env/bin/activate`
  
* **No Windows (CMD):**
  `.\.env\Scripts\activate`

* **No Windows (PowerShell):**
  `.\.env\Scripts\Activate.ps1`

> **Como saber se deu certo?** O nome `(.env)` aparecerá no início da linha do seu terminal.



---

## 📦 3. Gerenciamento de Pacotes com PIP

### `pip install`
* **Comando:** `pip install "fastapi[standard]"`
* **Objetivo:** Instala o framework FastAPI e o servidor Uvicorn.
* **Variação:** Se estiver em um ambiente com várias versões de Python, use `python -m pip install ...` para garantir que instale na versão correta.

### `pip list`
* **Objetivo:** Lista o que está instalado. Use para conferir se o FastAPI aparece na lista.

---

## 🛠️ 4. Utilidades e Editor

### `history`
* **Linux / PowerShell:** `history`
* **Windows (CMD):** `doskey /history`
* **Objetivo:** Ver os últimos comandos digitados. Ótimo para quando você esquece o que acabou de fazer.

### `code .`
* **Comando:** `code .`
* **Objetivo:** Abre o VS Code já focado na pasta atual. 
* **Dica:** Se o comando não funcionar, você precisa abrir o VS Code, apertar `Ctrl+Shift+P` e digitar "Shell Command: Install 'code' command in PATH".

---

## 🏃 5. Executando a API

### `fastapi dev`
* **Comando:** `fastapi dev main.py`
* **Objetivo:** Roda o servidor em modo de desenvolvimento.
* **Vantagem:** O modo `dev` observa seus arquivos. Se você mudar o código e salvar, ele reinicia o servidor automaticamente (**Hot Reload**).

---

## 📝 Resumo de Comandos Rápidos

| Ação            | Linux / Mac / Git Bash     | Windows (CMD)             |
| :-------------- | :------------------------- | :------------------------ |
| Criar Pasta     | `mkdir nome`               | `mkdir nome`              |
| Listar Arquivos | `ls -la`                   | `dir`                     |
| Criar Venv      | `python -m venv .env`      | `python -m venv .env`     |
| Ativar Venv     | `source .env/bin/activate` | `.\.env\Scripts\activate` |
| Ver Histórico   | `history`                  | `doskey /history`         |