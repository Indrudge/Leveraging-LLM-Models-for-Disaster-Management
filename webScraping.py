import requests
from bs4 import BeautifulSoup

def fetch_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [headline.text for headline in soup.find_all('h1')]  # Adjust the tag based on website structure
    return headlines