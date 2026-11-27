from typing import TypedDict, Annotated
from operator import add
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class State(TypedDict):
    #prompt do usuario
    prompt: str

    #plano do planejador
    plano: str

    #executor
    iteracoes_executor: int
    lista_trabalho: Annotated[list[str], add]
    pilha_do_executor: list[str]
    executor_quer_iterar: bool

    #revisor
    iteracoes_globais: int
    lista_revisoes: Annotated[list[str], add]
    revisor_quer_iterar: bool

    #mensagens gerais
    messages: Annotated[list[BaseMessage], add]

class RespostaPlanejador(BaseModel):
    """Resposta do nó de planajeamento"""
    plano: str = Field(description="o plano que foi gerado para resolver a tarefa proposta, um plano completo, detalhado e util, mas conciso")
    retorno: str = Field(description="um retorno simples de uma linha ao usuario para saber o que voce fez")

class RespostaRevisor(BaseModel):
    """Resposta do nó de revisão"""
    revisao: str = Field(description="uma revisão comentada sobre o que voce fez, com o intuito de ajudar o executor a fazer de novo o que esta errado, retorne 'nao a nada a corrigir' se julgar estar tudo certo")
    retorno: str = Field(description="um retorno simples de uma linha ao usuario para saber o que voce fez")
    iterar: bool = Field(description="se dejesa iterar com o executor para corrigir erros novamente, True para caso sim e False caso não")






