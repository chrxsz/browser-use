import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

load_dotenv()

# Initialize the model
llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)
task = 'Vá até a página https://reparador.fiat.com.br/ e siga os sseguintes passos:' \
'# Passo 1: vá para a página de login e faça o login com o seguinte usuário e senha: Login: testediagweb@gmail.com, Senha: Diag2025' \
'# Passo 2: selecione a opção Manutenção Fácil' \
'# Passo 3: selecione a marca Fiat, o carro Cronos, e o modelo 1.3 GSE FLEX MTA' \
'# Passo 4: selecione a opção Informações sobre serviços, e depois Esquemas elétricos, e baixe todos os diagramas elétricos'

agent = Agent(task=task, llm=llm)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
