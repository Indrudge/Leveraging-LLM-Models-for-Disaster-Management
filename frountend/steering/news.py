from django.http import JsonResponse
from pymongo import MongoClient, errors
import requests
import time
from datetime import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['news_db']
collection = db['disaster_news']

# API keys and URLs
GNEWS_API_KEY = '4db76ae70dfc1836064fdba572cc7d35'
NEWSAPI_KEY = '0dabb9421ff34ced94d506ebf1b4a2ed'
GNEWS_URL = 'https://gnews.io/api/v4/search'
NEWSAPI_URL = 'https://newsapi.org/v2/everything'

def filter_articles(articles):
    """Filter articles to only include those related to natural disasters in India."""
    filtered_articles = []
    for article in articles:
        # Check if both 'India' and 'natural disaster' are mentioned in the title, description, or content
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        content = article.get('content', '').lower()

        if 'india' in title and 'natural disaster' in title:
            filtered_articles.append(article)
        elif 'india' in description and 'natural disaster' in description:
            filtered_articles.append(article)
        elif 'india' in content and 'natural disaster' in content:
            filtered_articles.append(article)

    return filtered_articles

def fetch_gnews():
    """Fetch disaster news from GNews API."""
    all_articles = []
    page = 1
    while True:
        params = {
            'country': 'in',  # Limit to India
            'q': 'natural disaster',  # Focus on natural disaster-related news
            'lang': 'en',
            'apikey': GNEWS_API_KEY,
            'max': 10,
            'page': page
        }
        try:
            response = requests.get(GNEWS_URL, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get('articles', [])
            if not articles:
                break
            all_articles.extend(articles)
            page += 1
            time.sleep(1)
        except requests.exceptions.RequestException:
            break
    return all_articles

def fetch_newsapi():
    """Fetch disaster news from NewsAPI."""
    all_articles = []
    page = 1
    while True:
        params = {
            'q': 'natural disaster india',  # Search specifically for India-related natural disasters
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': NEWSAPI_KEY,
            'page': page,
            'pageSize': 100  # Maximum allowed value for NewsAPI
        }
        try:
            response = requests.get(NEWSAPI_URL, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get('articles', [])
            if not articles:
                break
            all_articles.extend(articles)
            page += 1
            time.sleep(1)
        except requests.exceptions.RequestException:
            break
    return all_articles

def insert_articles(articles):
    """Insert articles into MongoDB."""
    inserted_count = 0
    for article in articles:
        document = {
            'Title': article.get('title', 'No title'),
            'Description': article.get('description', 'No description'),
            'Date': article.get('publishedAt', 'Unknown'),
            'url': article.get('url', 'No URL'),
            'Content': article.get('content', 'No content'),
            'Source': article.get('source', {}).get('name', 'Unknown'),
        }
        try:
            # Use upsert to insert new or update existing articles
            collection.update_one({'url': document['url']}, {'$set': document}, upsert=True)
            inserted_count += 1
        except errors.PyMongoError:
            continue
    return inserted_count

def fetch_and_store_news():
    """Fetch news from APIs, filter them for natural disaster news in India, and store them in MongoDB."""
    gnews_articles = fetch_gnews()
    newsapi_articles = fetch_newsapi()

    # Filter articles for natural disasters in India
    filtered_gnews = filter_articles(gnews_articles)
    filtered_newsapi = filter_articles(newsapi_articles)

    # Combine the filtered articles
    combined_articles = filtered_gnews + filtered_newsapi

    # Insert the filtered articles into the database
    inserted_count = insert_articles(combined_articles)

    return JsonResponse({
        'message': 'Filtered news articles fetched and stored successfully.',
        'inserted_count': inserted_count
    })

