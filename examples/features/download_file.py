import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

load_dotenv()

llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)

browser = Browser(
	config=BrowserConfig(
		new_context_config=BrowserContextConfig(save_downloads_path=os.path.join(os.path.expanduser('~'), 'downloads'))
	)
)

models = ['ecosport', 'courier', 'edge', 'fiesta-rocam', 'focus', 'fusion', 'fusion-hibrido', 'ka', 'new-fiesta', 'new-fiesta-sedan', 'ranger']

years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015']

modelo = input('Selecione o modelo: ')
ano = input('Selecione o ano: ')

async def run_download():
	agent = Agent(
		task = (f"""
		  Você possui essa lista de modelos de carro: {models}, e essa lista de anos: {years}. Diante disso, você tem essa url 
		  base: https://www.reparadorford.com.br/motorcraft/informacoes-tecnicas/model/year/sistema-eletrico, e dessa url você pode mudar o endpoit de acordo com o pedido, no lugar de model, 
		  você troca por um modelo da lista models, e assim também com o year, você pode trocar por um ano da lista years. Depois desse processo, baixe o primeiro sistema elétrico. 
		  Caso seja necessário fazer login, faça com as seguintes credenciais: CPF = "406.967.091-20", senha = "Diag2025!". Assim, quero o sistema elétrico do modelo {modelo}, do ano {ano}.
		"""),
		llm=llm,
		max_actions_per_step=8,
		use_vision=True,
		browser=browser,
	)
	await agent.run(max_steps=25)
	await browser.close()


if __name__ == '__main__':
	asyncio.run(run_download())
