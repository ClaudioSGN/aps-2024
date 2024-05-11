import requests
from bs4 import BeautifulSoup
import json

def fetch_news(url, headline_tag, link_tag, class_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find specified headline tag then <a> within them
        news_items = [a for tag in soup.find_all(headline_tag) for a in tag.find_all(link_tag, href=True)]
        
        # Extracting news data and appending the source URL for identification
        news_data = [{'title': item.get_text(strip=True), 'link': item['href'], 'source': url} for item in news_items]
        return news_data
    except requests.RequestException as e:
        return str(e)

def save_news_to_json(news_data, filename='news_data.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(news_data, file, ensure_ascii=False, indent=4)

# URLs and their respective headline and link tag information
websites = [
    {'url': 'https://g1.globo.com/meio-ambiente/', 'headline_tag': 'h2', 'link_tag': 'a', 'class_name': 'feed-post-link'},
    {'url': 'https://www.cnnbrasil.com.br/tudo-sobre/meio-ambiente/', 'headline_tag': 'h3', 'link_tag': 'a', 'class_name': 'news-item'},
    {'url': 'https://www.bbc.com/portuguese/topics/c5qvpqj1dy4t', 'headline_tag': 'h2', 'link_tag': 'a', 'class_name': 'feed-post-link'},
    {'url': 'https://exame.com/noticias-sobre/meio-ambiente/', 'headline_tag': 'h3', 'link_tag': 'a', 'class_name': 'feed-post-link'}
]

all_news_data = []
for site in websites:
    news_data = fetch_news(site['url'], site['headline_tag'], site['link_tag'], site['class_name'])
    all_news_data.extend(news_data)

print(all_news_data)

# Save all fetched news data to JSON
save_news_to_json(all_news_data)
