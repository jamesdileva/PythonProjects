# News Tracker

A command line tool that fetches live breaking news using the NewsAPI.

## Features
- Top headlines — fetch the latest US headlines
- Headlines by category — business, entertainment, health, science, sports, technology
- Search by keyword — find articles on any topic
- Save results to file — export articles to a text report
- Live news ticker — auto-refreshing headlines with countdown timer

## Setup

### 1. Get a free API key
Sign up at [newsapi.org](https://newsapi.org) and copy your API key.

### 2. Create your .env file
Create a file called `.env` in the project folder:
```
NEWS_API_KEY=your_api_key_here
```

### 3. Install dependencies
```
pip install requests python-dotenv
```

### 4. Run the program
```
python news_tracker.py
```

## Security
This project uses a `.env` file to store the API key locally.
The `.env` file is excluded from GitHub via `.gitignore` and should
never be committed or shared.

## Roadmap
- **Horizontal scrolling marquee ticker** — terminal ticker tape effect
- **Multiple country support** — fetch headlines from any country
- **Sentiment analysis** — rate headlines as positive, negative, or neutral
- **Email digest** — automatically email a daily news summary
- **GUI interface** — desktop window with live updating headlines using Tkinter
- **Favorite topics** — save preferred categories and keywords between sessions
- **Article summarizer** — generate a one line summary of each article