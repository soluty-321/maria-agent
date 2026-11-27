import llm
from schermas import State
from tools import TOOLS_EXECUCAO
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import ToolNode


def no_inicio(state: State) -> dict:
    return {
        "iteracoes_globais": 3,
        "iteracoes_executor": 3,
        "lista_trabalho": [],
        "pilha_do_executor": [],
        "lista_revisoes": []
    }

def no_planejador(state: State) -> dict:
    prompt = [
        SystemMessage(content=llm.system_prompt),
        HumanMessage(content=f"voce é o planejador\n, sua tarefa é {state['prompt']}\n gere um plano util para o executor")
    ]
    planejador = llm.llm_planejador
    resposta = planejador.invoke(prompt)
    print(f"MARIA: {resposta.retorno}")
    return {
        "plano": resposta.plano
    }

def no_executor(state: State) -> dict:
    prompt = [
        SystemMessage(content=llm.system_prompt),
        HumanMessage(content=(
            f"Papel: Executor\n"
            f"tarefa: {state['prompt']}\n"
            f"Plano: {state['plano']}\n"
            f"o que voce ja fez: {state['pilha_do_executor']}\n"
            f"lista de revisoes (se tiver): {state['lista_revisoes']}"
            f"voce tem acesso a duas ferramentas\n"
            f"execute_code: executa codigo python e retorna stdout e erros\n"
            f"resposta_executor_estruturada: devolve o resultado de forma estruturada, use essa quando finalizar o trabalho\n"
            f"Iteraçoes restantes consigo mesmo: {state['iteracoes_executor']}\n"
            f"se quiser mais uma iteraçao, chame resposta_executor_estruturada com iterar=True, senao, com iterar=False"
        ))
    ] + state['messages']

    executor = llm.llm_executor
    resposta = executor.invoke(prompt)
    print(f"Tool chamada: {resposta.tool_calls[0]['name']}")
    return {
        "messages": [resposta]
    }

def no_rotear_apos_executor(state: State) -> dict:
    ultima = state['messages'][-1]
    nome = ultima.tool_calls[0]['name']
    if nome == "execute_code":
        return "tools"
    elif nome == "resposta_executor_estruturada":
        return "processar_resposta"

tool_node = ToolNode(TOOLS_EXECUCAO)

def processar_resposta(state: State) -> dict:
    ultima = state['messages'][-1]
    argumentos = ultima.tool_calls[0]["args"]

    mensagem = argumentos['retorno']
    print(f"MARIA: {mensagem}")

    trabalho = argumentos['trabalho']
    iterar = argumentos['iterar']

    if iterar and state["iteracoes_executor"] > 0:
        return {
            "messages": [ToolMessage(content="retorno recebido", tool_call_id=ultima.tool_calls[0]["id"])],
            "pilha_do_executor": state["pilha_do_executor"] + [trabalho],
            "iteracoes_executor": state["iteracoes_executor"] - 1,
            "executor_quer_iterar": True
        }
    elif not iterar or state["iteracoes_executor"] < 1:
        return {
            "messages": [ToolMessage(content="retorno recebido", tool_call_id=ultima.tool_calls[0]["id"])],
            "lista_trabalho": [trabalho],
            "pilha_do_executor": [],
            "executor_quer_iterar": False,
        }

def rotear(state: State):
    if state["executor_quer_iterar"]:
        return "executor"
    else:
        return "revisor"

def no_revisor(state: State) -> dict:
    prompt = [
        SystemMessage(content=llm.system_prompt),
        HumanMessage(content=(
            f"Papel: Revisor\n"
            f"tarefa: {state['prompt']}\n"
            f"Plano: {state['plano']}\n"
            f"o que ja foi feito {state['lista_trabalho']}"
            f"Iteraçoes restantes globais: {state['iteracoes_globais']}\n"
            f"itere se julgar necessario\n"
        ))
    ]

    revisor = llm.llm_revisor
    resposta = revisor.invoke(prompt)
    print(f"MARIA: {resposta.retorno}")
    return {
        "revisor_quer_iterar": resposta.iterar,
        "lista_revisoes": [resposta.revisao],
        "iteracoes_globais": state['iteracoes_globais'] - 1,
        "iteracoes_executor": 3
    }

def rotear_revisor(state: State):
    if state['revisor_quer_iterar'] and state["iteracoes_globais"] > 0:
        return "executor"
    else:
        return "final"

def final(state: State):
    print(f"MARIA: {state['lista_trabalho'][-1]}")
    print("Espero que tenha gostado mesmo nosso agente sendo extremamente primitivo e simples 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭")
    return

