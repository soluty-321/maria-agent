#M.A.R.I.A. Agent v0.0.3

import nodes
from schermas import State
from langgraph.graph import START, END, StateGraph

builder = StateGraph(State)

builder.add_node("inicio", nodes.no_inicio)
builder.add_node("planejador", nodes.no_planejador)
builder.add_node("executor", nodes.no_executor)
builder.add_node("processar_resposta", nodes.processar_resposta)
builder.add_node("revisor", nodes.no_revisor)
builder.add_node("fim", nodes.final)
builder.add_node("tool", nodes.tool_node)

builder.add_edge(START, "inicio")
builder.add_edge("inicio", "planejador")
builder.add_edge("planejador", "executor")

builder.add_conditional_edges(
    "executor",
    nodes.no_rotear_apos_executor,
    {
        "tools": "tool",
        "processar_resposta": "processar_resposta"
    }
)

builder.add_edge("tool", "executor")

builder.add_conditional_edges(
    "processar_resposta",
    nodes.rotear,
    {
        "executor": "executor",
        "revisor": "revisor"
    }
)

builder.add_conditional_edges(
    "revisor",
    nodes.rotear_revisor,
    {
        "executor": "executor",
        "final": "fim",
    }
)

graph = builder.compile()

prompt = input("Bem vindo ao MARIA(mecanismo autonomo e responsivo de intelegencia artificial), o que vamos fazer hoje?\n")
graph.invoke({"prompt": prompt})
