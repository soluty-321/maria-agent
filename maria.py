# M.A.R.I.A. Agent v0.0.2

from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Annotated
import operator
from pydantic import BaseModel, Field

class State(TypedDict):
    prompt: str
    plano: str
    iteracoes_globais: int
    iteracoes_executor: int
    lista_trabalho: Annotated[list[str], operator.add]
    lista_revisoes: Annotated[list[str], operator.add]
    executor_quer_iterar: bool
    revisor_quer_iterar: bool
    historico: Annotated[list[str], operator.add]
    pilha_do_executor: list[str]


class RespostaPlanejador(BaseModel):
    """Resposta do nó de planajeamento"""
    plano: str = Field(description="o plano que foi gerado para resolver a tarefa proposta, um plano completo, detalhado e util, mas conciso")
    retorno: str = Field(description="um retorno simples de uma linha ao usuario para saber o que voce fez")
    mensagem: str = Field(description="uma frase simples que serve como historico geral do agente")

class RespostaExecutor(BaseModel):
    """resposta do nó de execucao"""
    trabalho: str = Field(description="O que voce fez")
    retorno: str = Field(description="um retorno simples de uma linha ao usuario para saber o que voce fez")
    mensagem: str = Field(description="uma frase simples que serve como historico geral do agente")
    iterar: bool = Field(description="se voce deseja iterar novamente consigo mesmo (para, por exemplo, criar a resposta final em mais de uma etapa), se True, itera consigo mesmo, caso False segue para o revisor")

class RespostaRevisor(BaseModel):
    """Resposta do nó de revisão"""
    revisao: str = Field(description="uma revisão comentada sobre o que voce fez, com o intuito de ajudar o executor a fazer de novo o que esta errado, retorne 'nao a nada a corrigir' se julgar estar tudo certo")
    retorno: str = Field(description="um retorno simples de uma linha ao usuario para saber o que voce fez")
    mensagem: str = Field(description="uma frase simples que vserve como historico geral do agente")
    iterar: bool = Field(description="se dejesa iterar com o executor para corrigir erros novamente, True para caso sim e False caso não")

llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.1, reasoning_effort="medium")
llm_planejador = llm.with_structured_output(RespostaPlanejador)
llm_executor = llm.with_structured_output(RespostaExecutor)
llm_revisor = llm.with_structured_output(RespostaRevisor)

system_prompt = (
    f"voce é um asisstente de IA util chamado 'MARIA', Mecanismo autonomo e responsivo de inteligencia artificial\n"
    f"voce é util, conciso mas amigavel, lembre-se, voce tem nome Antropomórfico, trate o outro como um colega de trabalho, não como um usuario de sistema\n"
    f"no momento não temos tools calls disponiveis, resposta tudo só pensando\n"
)

def no_1(state: State) -> dict:
    return {"iteracoes_globais": 3, "iteracoes_executor": 3, "lista_trabalho": [], "lista_revisoes": [], "historico": [], "pilha_do_executor": []}

def no_2(state: State) -> dict:
    prompt1 = (
        system_prompt,
        f"voce é um planejador\nsua tarefa é essa {state['prompt']}\n",
        f"gere um plano para o executor"
    )
    resposta = llm_planejador.invoke(prompt1)
    print(f"MARIA: {resposta.retorno}")
    return {"plano": resposta.plano, "historico": [resposta.mensagem]}

def no_3(state: State) -> dict:
    prompt = (
        system_prompt,
        f"voce é um executor, sua tarefa é {state['prompt']}\n",
        f"siga o plano e faça o que foi pedido, voce pode fazer aos poucos e jogar na sua pilha de trabalho (caso iterar seja true) ou fazer tudo de uma vez\n"
        f"plano é {state['plano']}\n",
        f"a ultima revisao foi {state['lista_revisoes'][-1:]}\n",
        f"ultimo trabalho entregue {state['lista_trabalho'][-1:]}\n",
        f"sua pilha {state['pilha_do_executor']}\n",
        f"voce tem mais {state['iteracoes_executor']} iteracoes\n"
        f"ao final, junte tudo numa resposta só"
    )
    resposta = llm_executor.invoke(prompt)
    print(f"MARIA: {resposta.retorno}")
    print(f"LOGS: executor esta na iteracao {state['iteracoes_executor']}")
    if resposta.iterar and state["iteracoes_executor"] > 0:
        return {"pilha_do_executor": state["pilha_do_executor"] + [resposta.trabalho], "historico": [resposta.mensagem], "iteracoes_executor": state["iteracoes_executor"] - 1, "executor_quer_iterar": resposta.iterar}
    else:
        return {"pilha_do_executor": [], "historico": [resposta.mensagem], "lista_trabalho": [resposta.trabalho], "executor_quer_iterar": False}

def no_4(state: State):
    if state["executor_quer_iterar"]:
        return "iterar"
    else:
        return "revisao"

def no_5(state: State) -> dict:
    prompt = (
        system_prompt,
        f"voce é o revisor, sua tarefa é {state['prompt']}\n"
        f"revise o ultimo trabalho feito: {state['lista_trabalho'][-1:]}\n"
        f"seja um revisor util, faça criticas do que melhorar\n"
        f"voce pode iterar mais {state['iteracoes_globais']} com o executor\n"
    )

    resposta = llm_revisor.invoke(prompt)
    print(f"MARIA: {resposta.retorno}")
    if resposta.iterar and state["iteracoes_globais"] > 0:
        return {"historico": [resposta.mensagem], "lista_revisoes": [resposta.revisao], "revisor_quer_iterar": resposta.iterar, "iteracoes_globais": state["iteracoes_globais"] - 1, "iteracoes_executor": 3}
    else:
        return {"historico": [resposta.mensagem], "lista_revisoes": [resposta.revisao], "revisor_quer_iterar": False}

def no_6(state: State):
    if state["revisor_quer_iterar"]:
        return "iterar"
    else:
        return "entregar"

def no_7(state: State):
    print(f"MARIA: {state['lista_trabalho'][-1:]}")
    print("Espero que tenha gostado, mesmo nosso agente ainda sendo extremamente primitivo 😭😭😭😭😭")
    return {"lista_trabalho": ["concluido"]}

builder = StateGraph(State)

builder.add_node("inicio", no_1)
builder.add_node("planejador", no_2)
builder.add_node("executor", no_3)
builder.add_node("revisor", no_5)
builder.add_node("final", no_7)

builder.add_conditional_edges(
    "executor",
    no_4,
    {
        "iterar": "executor",
        "revisao": "revisor"
    }
)

builder.add_conditional_edges(
    "revisor",
    no_6,
    {
        "iterar": "executor",
        "entregar": "final"
    }
)

builder.add_edge(START, "inicio")
builder.add_edge("inicio", "planejador")
builder.add_edge("planejador", "executor")
builder.add_edge("final", END)

grafo = builder.compile()

pergunta = input("Bem vindo ao MARIA, seu assistente de IA, o que vamos fazer hoje?\n")
grafo.invoke({"prompt": pergunta})

    