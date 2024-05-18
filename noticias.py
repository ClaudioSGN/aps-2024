import requests
from bs4 import BeautifulSoup
import json

#Define uma função para buscar notícias de uma URL específica com manuseio de paginação para Agência Brasil
def fetch_news(url, headline_tag, link_tag, class_name, max_pages=10):
    news_data = []
    seen_titles = set()  #Para rastrear os títulos vistos e evitar duplicatas

    #Verifica se a URL é do site Agência Brasil
    if 'agenciabrasil.ebc.com.br' in url:
        #Loop para manusear a paginação até o número máximo de páginas especificado
        for page in range(1, max_pages + 1):
            paginated_url = f"{url}?page={page}"  #Constrói a URL da página paginada
            try:
                response = requests.get(paginated_url)  #Faz uma requisição GET para a URL paginada
                response.raise_for_status()  #Verifica se a requisição foi bem-sucedida
                soup = BeautifulSoup(response.text, 'html.parser')  #Parsea o HTML usando BeautifulSoup

                #Encontra todas as tags especificadas que contêm links e extrai esses links
                news_items = [a for tag in soup.find_all(headline_tag) for a in tag.find_all(link_tag, href=True)]
                print(f"Page {page} - Found {len(news_items)} items")  #Informação de depuração

                for item in news_items:
                    title = item.get_text(strip=True)
                    if title not in seen_titles:  #Verifica se o título ainda não foi visto
                        seen_titles.add(title)
                        #Filtra as notícias com base em palavras-chave no título
                        keywords = [
                            'meio ambiente', 'sustentabilidade', 'ecologia', 'natureza', 'poluição', 'enchente', 'chuvas',
                            'alagamento', 'queimadas', 'queimada', 'animais', 'desmatamento', 'clima',
                            'mudanças climáticas', 'fauna', 'flora', 'reflorestamento', 'reciclagem',
                            'biodiversidade', 'aquecimento global', 'impacto', 'ambiental', 'temperatura',
                            'temperaturas', 'frente fria', 'inundações', 'temporais', 'temporal', 'catástrofe',
                            'catástrofes', 'alerta', 'seca', 'secas', 'ecossistema', 'ecossistemas',
                            'risco', 'riscos', 'cheia', 'cheias'
                        ]
                        if any(keyword in title.lower() for keyword in keywords):
                            news_data.append({'title': title, 'link': item['href'], 'source': paginated_url})
                            print(f"Page {page} - Added news: {title}")  #Informação de depuração para cada notícia adicionada

                #Verifica se há um botão de próxima página
                next_page = soup.find('div', class_='item_list container').find('a', {'href': f'/tags/meio-ambiente?page={page+1}'})
                if not next_page:
                    break  #Sai do loop se não houver mais páginas
            except requests.RequestException as e:  #Captura exceções relacionadas a requisições HTTP
                print(f"Falha em encontrar notícias de: {paginated_url}: {e}")
                break  #Sai do loop se houver um erro ao buscar a página

    else:
        #Lógica para outros sites sem manuseio de paginação
        try:
            response = requests.get(url)  #Faz uma requisição GET para a URL
            response.raise_for_status()  #Verifica se a requisição foi bem-sucedida
            soup = BeautifulSoup(response.text, 'html.parser')  #Parsea o HTML usando BeautifulSoup

            #Encontra todas as tags especificadas que contêm links e extrai esses links
            news_items = [a for tag in soup.find_all(headline_tag) for a in tag.find_all(link_tag, href=True)]
            print(f"Achados {len(news_items)} itens")  #Informação de depuração

            for item in news_items:
                title = item.get_text(strip=True)
                if title not in seen_titles:  #Verifica se o título ainda não foi visto
                    seen_titles.add(title)
                    #Filtra as notícias com base em palavras-chave no título
                    keywords = [
                        'meio ambiente', 'sustentabilidade', 'ecologia', 'natureza', 'poluição', 'enchente', 'chuvas',
                        'alagamento', 'queimadas', 'queimada', 'animais', 'desmatamento', 'clima',
                        'mudanças climáticas', 'fauna', 'flora', 'reflorestamento', 'reciclagem',
                        'biodiversidade', 'aquecimento global', 'impacto', 'ambiental', 'temperatura',
                        'temperaturas', 'frente fria', 'inundações', 'temporais', 'temporal', 'catástrofe',
                        'catástrofes', 'alerta', 'seca', 'secas', 'ecossistema', 'ecossistemas',
                        'risco', 'riscos', 'cheia', 'cheias'
                    ]
                    if any(keyword in title.lower() for keyword in keywords):
                        news_data.append({'title': title, 'link': item['href'], 'source': url})
                        print(f"Added news: {title}")  #Informação de depuração para cada notícia adicionada
        except requests.RequestException as e:  #Captura exceções relacionadas a requisições HTTP
            print(f"Falha em encontrar notícias de: {url}: {e}")
    return news_data

#Define uma função para salvar os dados das notícias em um arquivo JSON
def save_news_to_json(news_data, filename='json/news_data.json'):
    with open(filename, 'w', encoding='utf-8') as file:  #Abre ou cria um arquivo JSON para escrita
        json.dump(news_data, file, ensure_ascii=False, indent=4)  #Escreve os dados no arquivo JSON de forma formatada

#Lista de websites de onde as notícias serão raspadas, junto com as tags HTML relevantes para localização das notícias
websites = [
    {'url': 'https://g1.globo.com/meio-ambiente/', 'headline_tag': 'h2', 'link_tag': 'a', 'class_name': 'feed-post-link'},
    {'url': 'https://agenciabrasil.ebc.com.br/tags/meio-ambiente', 'headline_tag': 'h4', 'link_tag': 'a', 'class_name': 'news-item'},
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
