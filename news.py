import requests
import sys
import os
import argparse
import json

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


class NewsAPIClient:
    def get_articles(self, url, params):
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json()["articles"]
        # print(json.dumps(articles, indent=2)) # pretty print
        return articles

    def get_sources(self, url, params):
        response = requests.get(url, params=params)
        response.raise_for_status()
        sources = response.json()["sources"]
        # print(json.dumps(sources, indent=2)) # pretty print
        return sources


def main():
    api_client = NewsAPIClient()
    parser = argparse.ArgumentParser(description="Get news from News API")
    parser.add_argument("action", choices=["category", "query", "sources"], help="Action to perform")
    parser.add_argument("value", help="Category, query, or country")

    args = parser.parse_args()

    if args.action == "category":
        if args.value in CATEGORIES:
            print_results(get_articles_by_category(args.value, api_client))
        else:
           print("Invalid category. Available categories:", ", ".join(CATEGORIES))
    elif args.action == "query":
        print_results(get_articles_by_query(args.value, api_client))
    elif args.action == "sources":
        print_sources_by_country(get_sources_by_country(args.value, api_client))



# Core functions for API requests and data processing


def get_articles_by_category(category, api_client):
    """Get top headlines by category."""
    query_parameters = {
        "category": category,
        "country": "us",
        "sortBy": "top",
        "apiKey": API_KEY,
    }
    return api_client.get_articles(URL_TOP_HEADLINES, query_parameters)


def get_articles_by_query(query, api_client):
    """Search for articles by query."""
    query_parameters = {
        "q": query,
        "language": "fr",
        "sortBy": "popularity",
        "apiKey": API_KEY,
    }
    return api_client.get_articles(URL_EVERYTHING, query_parameters)


def get_sources_by_country(country, api_client):
    """Get sources by country."""
    query_parameters = {
        "country": country,
        "apiKey": API_KEY,
    }
    return api_client.get_sources(URL_SOURCES, query_parameters)




def print_results(articles):
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

def print_sources_by_country(sources):
    results = [
        {
            "name": source["name"],
            "url": source["url"],
        }
        for source in sources
    ]
    for i, result in enumerate(results):
        print(i + 1, "-", result["name"], ":", result["url"])




if __name__ == "__main__":
    main()
