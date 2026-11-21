# M.A.R.I.A. v0.0.2
## Seu assistente pessoal alimentado por IA

M.A.R.I.A. (acronimo para Mecanismo Autonomo e Responsivo de Inteligencia Artificial) é um assistente pessoal baseado em inteligencia artificial baseado em grafos de estado.
Atualmente utilizando *langgraph* e modelos da *OpenAI*.

Diferentemente de ChatBots, M.A.R.I.A. resolve pedidos atraves de um fluxo estruturado de planajamento, execucao, revisao e iteracao.

## Como usar (linux)

clone o repositorio

```bash
git clone https://github.com/soluty-321/maria-agent
cd maria-agent
```

crie um ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate
```

instale as dependencias

```bash
pip install -r requirements.txt
```

configure sua chave da *OpenAI*

```bash
export OPENAI_API_KEY="sua chave"
```

execute o agente

```bash
python maria.py
```
## Novidades da 0.0.2

1. Scherma Pydantic separado para planejador, executor e revisor
2. Loop do executor com ele mesmo via pilha_do_executor

Desenvolvido as 22 horas por soluty-321, espero que gostem!