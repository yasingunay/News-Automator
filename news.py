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
        """Get articles from the specified URL with given parameters."""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            articles = response.json()["articles"]
            return articles
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return []

    def get_sources(self, url, params):
        """Get sources from the specified URL with given parameters."""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            sources = response.json()["sources"]
            return sources
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return []


def main():
    # Create an instance of the API client
    api_client = NewsAPIClient()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Get news from News API")
    parser.add_argument(
        "action", choices=["category", "query", "sources"], help="Action to perform"
    )
    parser.add_argument("value", help="Category, query, or country")
    parser.add_argument(
        "--language",
        help="Language mode is only avaiable for query search (e.g., 'en' for English, 'fr' for French)",
        default="en",
    )

    args = parser.parse_args()
    language = args.language

    if args.action == "category":
        if args.value in CATEGORIES:
            print_results(get_articles_by_category(args.value, api_client))
        else:
            print("Invalid category. Available categories:", ", ".join(CATEGORIES))
    elif args.action == "query":
        print_results(get_articles_by_query(args.value, language, api_client))
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


def get_articles_by_query(query, language, api_client):
    """Search for articles by query."""
    query_parameters = {
        "q": query,
        "language": language,
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


# Helper functions for printing results


def print_results(articles):
    """Print results."""
    results = [
        {
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "content": article["content"],
        }
        # Filter out articles with missing fields
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
    """Print sources by country."""
    results = [
        {
            "name": source["name"],
            "url": source["url"],
        }
        for source in sources
    ]
    # Print the results with an index
    for i, result in enumerate(results):
        print(i + 1, "-", result["name"], ":", result["url"])


if __name__ == "__main__":
    main()
