import os
from langchain_openai import AzureChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
#from langchain_experimental.tools.python import PythonREPL
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Modelo de linguagem do Azure OpenAI
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0
)

# Função de geração de testes
def unit_test_tool_func(code: str) -> str:
    template = """
    Você é um especialista em Python e testes automatizados.
    Gere testes unitários usando pytest para o seguinte código:
    ---
    {code}
    ---
    O teste deve cobrir:
    - Casos de sucesso
    - Casos de erro/exceções
    - Cenários com diferentes entradas
    Forneça apenas código Python válido.
    """
    prompt = PromptTemplate(template=template, input_variables=["code"])
    return llm.invoke(prompt.format(code=code)).content

# Ferramenta para execução de código Python
# python_repl_tool = Tool(
#     name="PythonREPL",
#     func=PythonREPL().run,
#     description="Executa código Python para cálculos ou verificação de comportamento de funções."
# )

# Ferramenta para geração de testes
unit_test_tool = Tool(
    name="GenerateUnitTests",
    func=unit_test_tool_func,
    description="Gera testes unitários pytest para o código Python fornecido."
)

# Inicializa o agente
agent = initialize_agent(
    tools=[unit_test_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def generate_tests(code: str) -> str:
    query = f"Analise o código e gere os testes unitários necessários:\n{code}"
    response = agent.run(query)
    return response
