import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

def extract_keywords(text):
    tokens = word_tokenize(text.lower())
    keywords = [word for word in tokens if word in ['disaster', 'flood', 'earthquake']]  # Add more keywords
    return keywords