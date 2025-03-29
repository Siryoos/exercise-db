# Exercise Crawler

A web application for crawling exercise data from [Virtuagym's exercise database](https://exercises.virtuagym.com/) using the Crawl4AI library.

## Features

- Web crawler for exercise categories, exercises, and exercise details
- Flask web interface with interactive UI
- Caching system to avoid unnecessary crawling
- Robust HTML parsing with fallback strategies
- Logging system for debugging
- Results export as JSON

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/exercise-crawler.git
   cd exercise-crawler
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Select a crawling task:
   - **Categories**: Get all exercise categories
   - **Category**: Get exercises in a specific category
   - **Exercise**: Get details of a specific exercise
   - **All**: Crawl all categories and exercises

4. Optional: Enter a URL for category or exercise tasks

5. Click "Start Crawling" to begin

6. View results and download as JSON

## Project Structure

```
exercise_crawler/
├── app.py              # Flask web application
├── crawler/
│   ├── __init__.py
│   ├── exercise_crawler.py  # Crawl4AI implementation
│   └── parser.py       # HTML parsing utilities
├── static/
│   └── style.css       # Simple styling
├── templates/
│   ├── index.html      # Main page
│   └── results.html    # Results display
├── utils/
│   ├── __init__.py
│   ├── cache.py        # Caching utilities
│   └── logger.py       # Logging configuration
└── requirements.txt    # Project dependencies
```

## Technical Details

### Crawler Module

The crawler module uses Crawl4AI to fetch web pages and parse exercise data. It includes methods for crawling different types of pages:

- Main page with exercise categories
- Category pages with lists of exercises
- Individual exercise pages with detailed information

The crawler supports caching to avoid repeated requests and can run with or without JavaScript rendering.

### Parser Module

The parser module extracts structured data from HTML using BeautifulSoup. It includes robust fallback strategies to handle different page structures.

### Caching System

The caching system stores crawled data in JSON files with configurable TTL (Time To Live). This improves performance and reduces load on the target server.

### Web Interface

The web interface is built with Flask and includes:

- Task selection interface
- URL input for specific tasks
- Result display with pretty-printed JSON
- JSON download functionality
- Cache management

## Advanced Usage

### API Endpoint

The application provides a simple API endpoint for crawling:

```bash
curl -X POST http://localhost:5000/api/crawl \
  -H "Content-Type: application/json" \
  -d '{"task": "main", "use_cache": true}'
```

### Cache Management

Clear the cache via API:

```bash
curl -X POST http://localhost:5000/api/clear-cache \
  -H "Content-Type: application/json" \
  -d '{}'
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
