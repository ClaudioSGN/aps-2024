import requests #Importa o módulo requests para fazer requisições HTTP
from bs4 import BeautifulSoup #Importa BeautifulSoup para parsear documentos HTML
import json #Importa o módulo json para trabalhar com dados JSON

#Define uma função para buscar notícias de uma URL específica
def fetch_news(url, headline_tag, link_tag, class_name):
    try:
        response = requests.get(url) #Faz uma requisição GET para a URL
        response.raise_for_status() #Verifica se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.text, 'html.parser') #Cria um objeto BeautifulSoup para parsear o HTML
        
        #Encontra todas as tags especificadas que contêm links e extrai esses links
        news_items = [a for tag in soup.find_all(headline_tag) for a in tag.find_all(link_tag, href=True)]
        
        #Cria uma lista de dicionários com os títulos das notícias, os links e a URL de origem
        news_data = [{'title': item.get_text(strip=True), 'link': item['href'], 'source': url} for item in news_items]
        return news_data
    except requests.RequestException as e: #Captura exceções relacionadas a requisições HTTP
        return str(e)

#Define uma função para salvar os dados das notícias em um arquivo JSON
def save_news_to_json(news_data, filename='news_data.json'):
    with open(filename, 'w', encoding='utf-8') as file: #Abre ou cria um arquivo JSON para escrita
        json.dump(news_data, file, ensure_ascii=False, indent=4) #Escreve os dados no arquivo JSON de forma formatada

#Lista de websites de onde as notícias serão raspadas, junto com as tags HTML relevantes para localização das notícias
websites = [
    {'url': 'https://g1.globo.com/meio-ambiente/', 'headline_tag': 'h2', 'link_tag': 'a', 'class_name': 'feed-post-link'},
    {'url': 'https://www.cnnbrasil.com.br/tudo-sobre/meio-ambiente/', 'headline_tag': 'h3', 'link_tag': 'a', 'class_name': 'news-item'},
    {'url': 'https://www.bbc.com/portuguese/topics/c5qvpqj1dy4t', 'headline_tag': 'h2', 'link_tag': 'a', 'class_name': 'feed-post-link'},
    {'url': 'https://exame.com/noticias-sobre/meio-ambiente/', 'headline_tag': 'h3', 'link_tag': 'a', 'class_name': 'feed-post-link'}
]

all_news_data = [] #Inicializa uma lista para armazenar dados de todas as notícias
for site in websites:
    news_data = fetch_news(site['url'], site['headline_tag'], site['link_tag'], site['class_name']) #Busca notícias para cada site
    all_news_data.extend(news_data) #Adiciona os dados das notícias à lista

print(all_news_data) #Imprime os dados coletados de todas as notícias

#Salva todas as notícias puxadas no arquivo: news_data.json
save_news_to_json(all_news_data)

#Este script faz automação do webscraping de notícias dos sites: G1, CNN, BBC e Exame usando a biblioteca 'requests'
#para realizar as requisições HTTP e 'BeautifulSoup' para o parser HTML. A função 'fetch_news' captura títulos, links e fontes
#de notícias com base em tags HTML específicas fornecidas para cada site. As notícias puxadas são enviadas para um arquivo .JSON
#por meio da função 'save_news_to_json'. A configuração inicial lista os URLs dos sites de notícias junto com as tags específicas
#para localizar as notícias, permitindo que seja possível alterar e adicionar facilmente uma nova fonte de notícias.