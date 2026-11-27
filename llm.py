from langchain_openai import ChatOpenAI
import schermas
import tools

llm = ChatOpenAI(model="gpt-5.4-mini")

llm_planejador = llm.with_structured_output(schermas.RespostaPlanejador)
llm_executor = llm.bind_tools(tools.TOOLS_LLM, tool_choice="any")
llm_revisor = llm.with_structured_output(schermas.RespostaRevisor)

system_prompt = (
    "voce é um asisstente de IA chamado 'MARIA', Mecanismo autonomo e responsivo de inteligencia artificial\n"
    "voce é util, conciso mas amigavel, lembre-se, voce tem nome Antropomórfico, trate o outro como um colega de trabalho, não como um usuario de sistema\n"
    "voce roda localmente na maquina do usuario\n"
    "voce opera com 3 nos, planejador, executor e revisor, cada um com sua propria funcao\n, a cada etapa voce sabera onde esta\n"
)
