import requests
import sys
import os
import argparse

# API documentation: https://newsapi.org/docs/endpoints/
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
    sys.exit(1)



def get_articles_by_category(category):
    """Get top headlines by category."""
    query_parameters = {
        "category": category,
        "country": "us",
        "sortBy": "top",
        "apiKey": API_KEY,
    }
    return _get_articles(URL_TOP_HEADLINES,query_parameters)


def get_articles_by_query(query):
    """Search for articles by query."""
    query_parameters = {
        "q": query,
        "language": "en",
        "sortBy": "popularity",
        "apiKey": API_KEY,  
    }
    return _get_everything(URL_EVERYTHING, query_parameters)


def _get_everything(url, params):
    response = requests.get(url, params=params)
    articles = response.json()["articles"]
    # print(json.dumps(sources, indent=2)) # pretty print

    results = [
        {
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "content": article["content"],
        }
        for article in articles
        if article["title"] is not None
        and article["description"] is not None
        and article["url"] is not None
    ]
    for result in results:
        print("Title        :", result["title"])
        print("Description  :", result["description"])
        print("Link         :", result["url"])
        print("")

    

def _get_articles(url, params):
    """Internal function to fetch and display articles."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        articles = response.json()["articles"]
        #print(json.dumps(articles, indent=2))  # pretty print

        results = [
            {
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "content": article["content"],
            }
            for article in articles
            if article["title"] is not None
            and article["description"] is not None
            and article["url"] is not None
        ]
        for result in results:
            print("Title        :", result["title"])
            print("Description  :", result["description"])
            print("Link         :", result["url"])
            print("")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")



def _get_sources(url, params):
    """Internal function to fetch and display sources."""
    response = requests.get(url, params=params)
    sources = response.json()["sources"]
    # print(json.dumps(sources, indent=2)) # pretty print

    results = [
        {
            "name": source["name"],
            "url": source["url"],
        }
        for source in sources
    ]
    for i, result in enumerate(results):
        print(i + 1, "-", result["name"], ":", result["url"])


def get_sources_by_country(country):
    """Get sources by country."""
    query_parameters = {
        "country": country,
        "apiKey": API_KEY,
    }
    return _get_sources(URL_SOURCES, query_parameters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get news from News API")
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
