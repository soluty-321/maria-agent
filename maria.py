# M.A.R.I.A. Agent v0.0.1

from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Annotated
import operator
from pydantic import BaseModel, Field

class State(TypedDict):
    prompt: str
    historico: Annotated[list[str], operator.add]
    trabalho: Annotated[list[str], operator.add]
    iteracoes: int
    iteracao: bool

class Resposta(BaseModel):
    """Resposta do Modelo"""
    resposta: str = Field(description="o que voce fez/ o que foi pedido")
    anotacao: str = Field(description="uma anotacao sobre o que voce fez, frase curta mas util")
    retorno: str = Field(description="essa frase será printada para o usuario saber o que voce esta fazendo no momento, uma frase util e curta")
    iteracao: bool = Field(description="se precisa ou não iterar novamente ao nó de execucao, só cabe ao nó de revisao, caso voce não for o nó de revisao, retorne False")

llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)
llm_estruturado = llm.with_structured_output(Resposta)


def inicio(state: State) -> dict:
    return {"historico": [], "trabalho": [], "iteracoes": 4, "iteracao": False}

def no_1(state: State) -> dict:
    promt = (
        f"voce é um agente de IA prestativo e conciso, Chamado MARIA(mecanismo autonomo de resolucao por inteligencia artificial)\n"
        f"a sua tarefa agora é {state['prompt']}\n"
        f"voce é o nó de planajamento do grafo, sua funcão é gerar o plano que os outros nós irao executar\n"
        f"gere um plano conciso mas util e detalhado\n"
        f"no momento não temos tools disponiveis, ou seja, resolva tudo só pensando\n"
    )
    saida = llm_estruturado.invoke(promt)
    print(saida.retorno)
    return {"historico": [saida.anotacao], "trabalho": [saida.resposta]}

def no_2(state: State) -> dict:
    promt = (
        f"voce é um agente de IA prestativo e conciso, Chamado MARIA(mecanismo autonomo de resolucao por inteligencia artificial)\n"
        f"a sua tarefa agora é {state['prompt']}\n"
        f"voce é o nó de execucao do grafo, sua funcao é executar o que o plano pediu e corrigir o que ja foi feito com base nas notas do revisor(se as notas existirem)\n"
        f" o que ja foi feito anteriormente: {state['trabalho']}\n"
        f"o que foi deixado de aviso: {state['historico']}\n"
        f"resolva de forma simples, sem overengineering, mas de forma correta segundo o planejamento\n"
        f"no momento não temos tools disponiveis, ou seja, resolva tudo só pensando\n"
    )
    saida = llm_estruturado.invoke(promt)
    print(saida.retorno)
    return {"historico": [saida.anotacao], "trabalho": [saida.resposta], "iteracoes": state["iteracoes"] - 1}

def no_3(state: State) -> dict:
    promt = (
        f"voce é um agente de IA prestativo e conciso, Chamado MARIA(mecanismo autonomo de resolucao por inteligencia artificial)\n"
        f"a sua tarefa agora é {state['prompt']}\n"
        f"voce é o nó de revisao do grafo, sua funcao é analisar a ultima saida, ver erros e conformidades com o plano\n"
        f" o que ja foi feito anteriormente: {state['trabalho']}\n"
        f"o que foi deixado de aviso: {state['historico']}\n"
        f"gere uma revisao completa, consica e detalhada, mas util\n"
        f"no campo 'iteracao', responda True caso precise iterar para o executou, ou False se não precisar\n"
        f"no momento não temos tools disponiveis, ou seja, resolva tudo só pensando\n"
    )
    saida = llm_estruturado.invoke(promt)
    print(saida.retorno)
    return {"historico": [saida.anotacao], "trabalho": [saida.resposta], "iteracao": saida.iteracao}

def decisao(state: State):
    if state["iteracao"] == True and state['iteracoes'] > 0:
        return True
    else:
        return False

def no_4(state: State) -> dict:
    print(f"a resposta do modelo foi: {state['trabalho'][-2]}")
    print("espero que tenha gostado, desculpe pelo agente ser extramente primitivo 😭😭😭")
    return {"trabalho": ["concluido"]}

builder = StateGraph(State)

builder.add_node("inicio", inicio)
builder.add_node("planejamento", no_1)
builder.add_node("execucao", no_2)
builder.add_node("revisor", no_3)
builder.add_node("fim", no_4)

builder.add_conditional_edges(
    "revisor",
    decisao,
    {
        True: "execucao",
        False: "fim"
    }
)

builder.add_edge(START, "inicio")
builder.add_edge("inicio", "planejamento")
builder.add_edge("planejamento", "execucao")
builder.add_edge("execucao", "revisor")
builder.add_edge("fim", END)

grafo = builder.compile()

pergunta = input("Bem vindo ao MARIA(Mecanismo Autonomo e Responsivo de Inteligencia Artificial), seu assistente pessoal!, o que vamos fazer hoje?\n")
grafo.invoke({"prompt": pergunta})






    