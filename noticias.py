import requests  #Importa a biblioteca requests para fazer requisições HTTP
from bs4 import BeautifulSoup  #Importa BeautifulSoup para parsear o HTML
import json  #Importa a biblioteca json para trabalhar com dados JSON

#Define uma função para buscar notícias de uma URL específica com paginação para o site da CNN Brasil
def fetch_news(url, headline_tag, link_tag, class_name):
    news_data = []  #Inicializa uma lista para armazenar os dados das notícias
    if "cnnbrasil.com.br" in url:  #Verifica se a URL é do site da CNN Brasil
        #Lida com a paginação para o site da CNN Brasil
        for page in range(1, 21):  #Busca até 20 páginas
            paginated_url = f"{url}pagina/{page}/"  #Constrói a URL paginada
            try:
                response = requests.get(paginated_url)  #Faz a requisição HTTP
                response.raise_for_status()  #Verifica se a requisição foi bem-sucedida
                soup = BeautifulSoup(response.text, 'html.parser')  #Parseia o HTML da página

                #Encontra todas as tags especificadas contendo links e extrai esses links
                news_items = [a for tag in soup.find_all(headline_tag) for a in tag.find_all(link_tag, href=True)]

                for item in news_items:
                    title = item.get_text(strip=True)  #Extrai o texto do título da notícia
                    #Filtra as notícias com base em palavras-chave no título
                    keywords = ['meio ambiente', 'sustentabilidade', 'ecologia', 'natureza', 'poluição', 'enchente', 'chuvas', 'alagamento', 'queimadas', 'queimada', 'animais', 'ecologia', 'desmatamento', 'clima', 'mudanças climáticas', 'fauna', 'flora', 'reflorestamento', 'poluição', 'reciclagem', 'biodiversidade', 'aquecimento global', 'impacto', 'ambiental', 'natureza', 'temperatura', 'temperaturas', 'frente fria', 'inundações', 'temporais', 'temporal', 'catástrofe', 'catástrofes', 'alerta', 'enchentes', 'seca', 'secas', 'ecossistema', 'ecossistemas', 'risco', 'riscos', 'cheia', 'cheias']
                    if any(keyword in title.lower() for keyword in keywords):  #Verifica se alguma palavra-chave está no título
                        news_data.append({'title': title, 'link': item['href'], 'source': paginated_url})  #Adiciona a notícia à lista
            except requests.RequestException as e:  #Captura exceções relacionadas a requisições HTTP
                print(f"Failed to fetch news from {paginated_url}: {e}")  #Imprime uma mensagem de erro
    else:
        #Lida com outros sites sem paginação
        try:
            response = requests.get(url)  #Faz a requisição HTTP
            response.raise_for_status()  #Verifica se a requisição foi bem-sucedida
            soup = BeautifulSoup(response.text, 'html.parser')  #Parseia o HTML da página

            #Encontra todas as tags especificadas contendo links e extrai esses links
            news_items = [a for tag in soup.find_all(headline_tag) for a in tag.find_all(link_tag, href=True)]

            for item in news_items:
                title = item.get_text(strip=True)  #Extrai o texto do título da notícia
                #Filtra as notícias com base em palavras-chave no título
                keywords = ['meio ambiente', 'sustentabilidade', 'ecologia', 'natureza', 'poluição', 'enchente', 'chuvas', 'alagamento', 'queimadas', 'queimada', 'animais', 'ecologia', 'desmatamento', 'clima', 'mudanças climáticas', 'fauna', 'flora', 'reflorestamento', 'poluição', 'reciclagem', 'biodiversidade', 'aquecimento global', 'impacto', 'ambiental', 'natureza', 'temperatura', 'temperaturas', 'frente fria', 'inundações', 'temporais', 'temporal', 'catástrofe', 'catástrofes', 'alerta', 'enchentes', 'seca', 'secas', 'ecossistema', 'ecossistemas', 'risco', 'riscos', 'cheia', 'cheias']
                if any(keyword in title.lower() for keyword in keywords):  #Verifica se alguma palavra-chave está no título
                    news_data.append({'title': title, 'link': item['href'], 'source': url})  #Adiciona a notícia à lista
        except requests.RequestException as e:  #Captura exceções relacionadas a requisições HTTP
            return str(e)
    return news_data

#Define uma função para salvar os dados das notícias em um arquivo JSON
def save_news_to_json(news_data, filename='news_data.json'):
    with open(filename, 'w', encoding='utf-8') as file:  #Abre ou cria um arquivo JSON para escrita
        json.dump(news_data, file, ensure_ascii=False, indent=4)  #Escreve os dados no arquivo JSON de forma formatada

#Lista de websites de onde as notícias serão raspadas, junto com as tags HTML relevantes para localização das notícias
websites = [
    {'url': 'https://g1.globo.com/meio-ambiente/', 'headline_tag': 'h2', 'link_tag': 'a', 'class_name': 'feed-post-link'},
    {'url': 'https://www.cnnbrasil.com.br/tudo-sobre/meio-ambiente/', 'headline_tag': 'h3', 'link_tag': 'a', 'class_name': 'news-item'},
    {'url': 'https://www.bbc.com/portuguese/topics/c5qvpqj1dy4t', 'headline_tag': 'h2', 'link_tag': 'a', 'class_name': 'feed-post-link'},
    {'url': 'https://exame.com/noticias-sobre/meio-ambiente/', 'headline_tag': 'h3', 'link_tag': 'a', 'class_name': 'feed-post-link'}
]

all_news_data = []  #Inicializa uma lista para armazenar dados de todas as notícias
for site in websites:
    news_data = fetch_news(site['url'], site['headline_tag'], site['link_tag'], site['class_name'])  #Busca notícias para cada site
    all_news_data.extend(news_data)  #Adiciona os dados das notícias à lista

print(all_news_data)  #Imprime os dados coletados de todas as notícias

#Salva todas as notícias puxadas no arquivo: news_data.json
save_news_to_json(all_news_data)

#Este código faz o scraping das notícias do site G1, CNN, BBC e Exame
#com a função "fetch_news" onde também especifica as keywords(palavras-chave)
#para que o scrap não seja notícias não relacionadas ao tema de meio-ambiente
#após coletar todas as notícias de todos os sites, o código armazena todas em um
#arquivo .JSON chamado: "news_data.json" para que seja utilizado no "ai_analyzer"
#onde as notícias serão classificadas e separadas para a porcentagem gerada no gráfico.