import requests
import os
import time
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.environ.get("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"

def get_top_headlines(category="general"):
    url = f"{BASE_URL}/top-headlines"
    params = {
        "apiKey": API_KEY,
        "country": "us",
        "category": category,
        "pageSize": 10
    }
    response = requests.get(url, params=params)
    return response.json()

def get_keyword_news(keyword):
    url = f"{BASE_URL}/everything"
    params = {
        "apiKey": API_KEY,
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10
    }
    response = requests.get(url, params=params)
    return response.json()

def display_articles(data):
    if data.get("status") != "ok":
        print(f"\n⚠ Error fetching news: {data.get('message', 'Unknown error')}")
        return
    
    articles = data.get("articles", [])
    if not articles:
        print("\nNo articles found.")
        return

    print(f"\n--- {len(articles)} Articles Found ---")
    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        source = article.get("source", {}).get("name", "Unknown source")
        published = article.get("publishedAt", "")
        url = article.get("url", "")

        if published:
            published = published[:10]

        print(f"\n{i}. {title}")
        print(f"   Source: {source} | Date: {published}")
        print(f"   URL: {url}")

def save_articles(data, filename):
    if data.get("status") != "ok":
        print("\n⚠ No articles to save.")
        return

    articles = data.get("articles", [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"News Report — {timestamp}\n")
        f.write("=" * 40 + "\n\n")
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            published = article.get("publishedAt", "")[:10]
            url = article.get("url", "")
            description = article.get("description", "No description available")

            f.write(f"{i}. {title}\n")
            f.write(f"   Source: {source} | Date: {published}\n")
            f.write(f"   {description}\n")
            f.write(f"   URL: {url}\n\n")

    print(f"\n✓ Articles saved to {filename}")

def run_ticker(interval_minutes=30):
    interval_seconds = interval_minutes * 60
    print(f"\n🗞 Starting News Ticker — refreshing every {interval_minutes} minutes")
    print("Press Ctrl+C at any time to return to the main menu\n")

    try:
        while True:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n{'='*50}")
            print(f"  LIVE HEADLINES — Updated at {timestamp}")
            print(f"{'='*50}")

            data = get_top_headlines()
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                for i, article in enumerate(articles, 1):
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "Unknown")
                    print(f"\n{i}. {title}")
                    print(f"   — {source}")
            else:
                print(f"\n⚠ Error: {data.get('message', 'Unknown error')}")

            print(f"\n{'='*50}")
            print(f"Next update in {interval_minutes} minutes — Press Ctrl+C to exit ticker")

            for remaining in range(interval_seconds, 0, -1):
                mins, secs = divmod(remaining, 60)
                print(f"  Refreshing in {mins:02d}:{secs:02d}", end="\r")
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n✓ Ticker stopped — returning to main menu")
        
def main():
    print("Welcome to News Tracker")

    if not API_KEY:
        print("\n⚠ API key not found. Make sure your .env file is set up correctly.")
        return

    last_data = None

    while True:
        print("\nWhat would you like to do?")
        print("1. Top Headlines")
        print("2. Headlines by Category")
        print("3. Search by Keyword")
        print("4. Save Last Results to File")
        print("5. Live News Ticker")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ")

        if choice == "1":
            last_data = get_top_headlines()
            display_articles(last_data)

        elif choice == "2":
            print("\nCategories: business, entertainment, health, science, sports, technology")
            category = input("Enter category: ").strip().lower()
            last_data = get_top_headlines(category)
            display_articles(last_data)

        elif choice == "3":
            keyword = input("Enter keyword to search: ").strip()
            if keyword:
                last_data = get_keyword_news(keyword)
                display_articles(last_data)
            else:
                print("\nPlease enter a keyword.")

        elif choice == "4":
            if last_data:
                filename = input("Enter filename (e.g. news_report.txt): ").strip()
                if filename:
                    save_articles(last_data, filename)
                else:
                    print("\nPlease enter a filename.")
            else:
                print("\nNo results to save yet. Fetch some news first.")

        elif choice == "5":
            print("\nRefresh interval options:")
            print("1. Every 15 minutes")
            print("2. Every 30 minutes (default)")
            print("3. Every 60 minutes")
            interval_choice = input("\nEnter choice (1-3) or press Enter for default: ").strip()

            if interval_choice == "1":
                interval = 15
            elif interval_choice == "3":
                interval = 60
            else:
                interval = 30

            run_ticker(interval)

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1-6.")

main()
