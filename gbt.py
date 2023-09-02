import os
import requests
import argparse

# Constants
URL_EVERYTHING = "https://newsapi.org/v2/everything"
URL_TOP_HEADLINES = "https://newsapi.org/v2/top-headlines"
URL_SOURCES = "https://newsapi.org/v2/top-headlines/sources"

CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]

# Get the API key from the environment variable
API_KEY = os.getenv("NEWS_API_KEY")
if API_KEY is None:
    print("Please set the NEWS_API_KEY environment variable.")
    exit(1)

def get_articles_by_category(category):
    """Get top headlines by category."""
    params = {
        "category": category,
        "country": "us",
        "sortBy": "top",
        "apiKey": API_KEY,
    }
    return _get_articles(URL_TOP_HEADLINES, params)

def get_articles_by_query(query):
    """Search for articles by query."""
    params = {
        "q": query,
        "language": "en",
        "sortBy": "popularity",
        "apiKey": API_KEY,  
    }
    return _get_articles(URL_EVERYTHING, params)

def _get_articles(url, params):
    """Internal function to fetch and display articles."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        articles = response.json().get("articles", [])
        
        for article in articles:
            if all(article.get(field) for field in ["title", "description", "url"]):
                print("Title       :", article["title"])
                print("Description :", article["description"])
                print("Link        :", article["url"])
                print("")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        
def get_sources_by_country(country):
    """Get news sources by country."""
    params = {
        "country": country,
        "apiKey": API_KEY,
    }
    _get_sources(URL_SOURCES, params)

def _get_sources(url, params):
    """Internal function to fetch and display news sources."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        sources = response.json().get("sources", [])
        
        for i, source in enumerate(sources, start=1):
            print(f"{i} - {source['name']} : {source['url']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="News API Client")
    parser.add_argument("action", choices=["category", "query", "sources"], help="Action to perform")
    parser.add_argument("value", help="Category, query, or country")

    args = parser.parse_args()

    if args.action == "category":
        if args.value in CATEGORIES:
            get_articles_by_category(args.value)
        else:
            print("Invalid category. Available categories:", ", ".join(CATEGORIES))
    elif args.action == "query":
        get_articles_by_query(args.value)
    elif args.action == "sources":
        get_sources_by_country(args.value)
