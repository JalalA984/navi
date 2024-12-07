import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class Article(object):
    def __init__(self, article_json):
        self.title = article_json["title"]
        self.description = article_json.get("description")
        self.url = article_json["url"]
        self.source = article_json["source"]["name"]
        self.published_at = datetime.fromisoformat(article_json["publishedAt"].replace("Z", "+00:00"))
        self.content = article_json.get("content")
        self.urlToImage = article_json.get("urlToImage")

    def __repr__(self):
        return self.title

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "source": self.source,
            "published_at": self.published_at.isoformat(),
            "content": self.content,
            "urlToImage": self.urlToImage
        }


class NaviNewsClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        self.base_url = "https://newsapi.org/v2/"
        self.api_key = api_key
        self.headers = {"X-Api-Key": self.api_key}

    def search_articles(self, query, from_date=None, to_date=None, language="en", sort_by="publishedAt", page=1, page_size=20):
        """
        Searches for news articles based on the given query and parameters.
        """
        search_url = f"{self.base_url}everything"
        
        params = {
            "q": query,
            "language": language,
            "sortBy": sort_by,
            "page": page,
            "pageSize": page_size
        }
        
        if from_date:
            params["from"] = from_date.isoformat()
        if to_date:
            params["to"] = to_date.isoformat()

        resp = self.sess.get(search_url, params=params, headers=self.headers)

        if resp.status_code != 200:
            raise ValueError(f"Search request failed with status code {resp.status_code}. Response: {resp.text}")

        data = resp.json()

        if data["status"] != "ok":
            raise ValueError(f'[ERROR]: Error retrieving results: {data.get("message", "Unknown error")}')

        articles = [Article(article_json) for article_json in data["articles"]]
        return articles, data["totalResults"]

    def get_top_headlines(self, country="us", category=None, query=None, page=1, page_size=20):
        """
        Retrieves top headlines based on the specified parameters.
        """
        headlines_url = f"{self.base_url}top-headlines"
        
        params = {
            "country": country,
            "page": page,
            "pageSize": page_size
        }
        
        if category:
            params["category"] = category
        if query:
            params["q"] = query

        resp = self.sess.get(headlines_url, params=params, headers=self.headers)

        if resp.status_code != 200:
            raise ValueError(f"Request for top headlines failed with status code {resp.status_code}. Response: {resp.text}")

        data = resp.json()

        if data["status"] != "ok":
            raise ValueError(f'[ERROR]: Error retrieving results: {data.get("message", "Unknown error")}')

        articles = [Article(article_json) for article_json in data["articles"]]
        return articles, data["totalResults"]

# Example usage
if __name__ == "__main__":
    import os

    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        raise ValueError("NEWS_API_KEY environment variable is not set")

    client = NaviNewsClient(api_key)

    # Search for articles
    query = "technology"
    try:
        articles, total_results = client.search_articles(query, from_date=datetime.now() - timedelta(days=7))
        print(f"Search Results for '{query}':")
        for article in articles[:5]:  # Print first 5 articles
            print(f"- {article.title}")
            print(f"  Published: {article.published_at}")
            print(f"  Source: {article.source}")
            print(f"  URL: {article.url}")
            print()
        print(f"Total articles found: {total_results}")
    except ValueError as e:
        print(f"Error searching articles: {e}")

    print("\nTop Headlines:")
    try:
        # Get top headlines
        headlines, total_headlines = client.get_top_headlines(category="technology")
        for headline in headlines[:5]:  # Print first 5 headlines
            print(f"- {headline.title}")
            print(f"  Published: {headline.published_at}")
            print(f"  Source: {headline.source}")
            print(f"  URL: {headline.url}")
            print()
        print(f"Total headlines found: {total_headlines}")
    except ValueError as e:
        print(f"Error getting top headlines: {e}")
