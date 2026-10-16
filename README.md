# M.A.R.I.A. v0.0.1
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

Desenvolvido as 22 horas por soluty-321 de 15 anos, espero que gostem! Logo sai a versão v0.0.2!