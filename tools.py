from langchain_core.tools import tool
from typing import Annotated
import sys
import io

memoria = {}

@tool
def execute_code(code: str) -> str:
    """Executa o código Python fornecido e retorna a saída ou erros."""
    # Redireciona stdout para capturar a saída do código
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    try:
        exec(code, memoria)  
        output = new_stdout.getvalue()
    except Exception as e:
        output = new_stdout.getvalue() + f"Erro ao executar o código: {e}"
    finally:
        # Restaura stdout
        sys.stdout = old_stdout

    return output


@tool
def resposta_executor_estruturada(
    trabalho: Annotated[str, "O que voce fez"],
    retorno: Annotated[str, "um retorno simples de uma linha ao usuario para saber o que voce fez"],
    iterar: Annotated[bool, "e voce deseja iterar novamente consigo mesmo"],
) -> str:
    """retorno estruturado do executor, não executa nada diretamente, chame quando o trabalho for concluido"""
    return "retorno recebido"

TOOLS_EXECUCAO = [execute_code]                    
TOOLS_LLM = [execute_code, resposta_executor_estruturada]  