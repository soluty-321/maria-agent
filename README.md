# M.A.R.I.A. v0.0.3
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
## Novidades da 0.0.3

1. Finalmente Temos Tools! Introduzida uma tool de execução de codigo python (execute_code)
2. Codigo modularizado em 5 arquivos, llm.py, nodes.py, schermas.py, tools.py e maria.py
3. Schema pydantic do executor foi tranformado numa tool
4. Aplicação do sistema de Mensagens (messages) do *langchain*

Desenvolvido por soluty-321, espero que gostem!