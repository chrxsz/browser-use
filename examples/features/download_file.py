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
systems = ['carroceria', 'motor', 'semi-arvores', 'sistema-de-combustivel', 'sistema-de-direcao', 'sistema-de-escapamento', 'sistema-de-freio', 'sistema-de-transmissao', 'sistema-eletrico', 'suspensao', 'informacoes-gerais']

input_user = input("Defina aqui o que você quer: ")

async def run_download():
	agent = Agent(
		task = (f"""
		 	Você é um agente destinado a ajudar pessoas com problemas em carros da marca Ford. Seu objetivo é entender o que o usuário está precisando e retornar o material técnico mais adequado, 
			realizando uma busca no site do Reparador Ford. Existem duas maneiras possíveis para essa busca:

			# Maneira 1 - Busca por URL estruturada:
			Você pode utilizar a seguinte URL base: https://www.reparadorford.com.br/motorcraft/informacoes-tecnicas/model/year/system
			As palavras `model`, `year` e `system` são variáveis que devem ser substituídas por termos correspondentes às listas {models}, {years} e {systems}, respectivamente. Analise o pedido do usuário e escolha os termos mais apropriados para cada variável. 
			Caso mais de um termo se aplique bem ao contexto, você pode usar múltiplos valores separados por dois-pontos, como neste exemplo: `modelo1:modelo2:modelo3`
			Após definir a URL, acesse o site e baixe o arquivo que mais se relaciona com o problema do usuário. Você pode rolar a página, clicar em "carregar mais arquivos" e navegar livremente para encontrar o melhor resultado.

			# Maneira 2 - Busca por expressão:
			Utilize a seguinte URL base: https://www.reparadorford.com.br/motorcraft/informacoes-tecnicas?busca=expressao
			Substitua a palavra `expressao` por uma frase ou palavra-chave que resuma da melhor forma o pedido do usuário. 
			Após definir a URL, realize a busca, baixe o arquivo mais relevante, considerando sempre o modelo, ano e problema descrito pelo usuário. Você também pode rolar a página e carregar mais arquivos, se necessário.

			## Observações importantes:
			- Sempre analise o pedido do usuário com atenção para evitar alucinações;
			- Escolha livremente entre a Maneira 1 ou a Maneira 2, conforme o caso;
			- Usar somente as Urls fornecidas, podendo ser alteradas de acordo com o pedido do usuário;
			- Se o site solicitar login, use as seguintes credenciais:
				- CPF: 406.967.091-20
				- Senha: Diag2025!

			A seguir está o pedido do usuário:
			{input_user}
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
