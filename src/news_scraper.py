from newsapi import NewsApiClient
import json
from datetime import datetime, timedelta

class NewsScraper:
    def __init__(self, api_key):
        self.newsapi = NewsApiClient(api_key=api_key)
    
    def get_stock_news(self, company_name, days=7):
        """Get recent news for a stock"""
        try:
            articles = self.newsapi.get_everything(
                q=f"{company_name} stock market",
                language='en',
                sort_by='publishedAt',
                page_size=20
            )
            
            return articles.get('articles', [])
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def extract_text(self, articles):
        """Extract title + description"""
        texts = []
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}"
            texts.append(text)
        return texts