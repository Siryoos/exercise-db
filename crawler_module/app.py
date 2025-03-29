import os
import json
from flask import Flask, render_template, request, jsonify
import logging

from crawler.exercise_crawler import ExerciseCrawler
from utils.cache import CacheManager
from utils.logger import setup_logger

# Setup logging
setup_logger()
logger = logging.getLogger(__name__)

app = Flask(__name__)
cache = CacheManager(ttl=3600)  # 1 hour cache

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/crawl', methods=['POST'])
def crawl():
    """API endpoint for crawling"""
    data = request.json
    task = data.get('task', 'main')
    url = data.get('url')
    use_cache = data.get('use_cache', True)
    
    # Generate cache key
    cache_key = f"{task}:{url}" if url else task
    
    # Try to get from cache
    if use_cache:
        cached_result = cache.get(cache_key)
        if cached_result:
            return jsonify({
                'success': True,
                'from_cache': True,
                'result': cached_result
            })
    
    # Initialize crawler
    crawler = ExerciseCrawler(
        headless=True,
        js_render=True,
        bypass_cache=not use_cache
    )
    
    # Run crawler
    result = crawler.run_crawler(task, url)
    
    # Cache result if successful
    if result.get('success', False) and use_cache:
        cache.set(cache_key, result)
    
    return jsonify({
        'success': True,
        'from_cache': False,
        'result': result
    })

@app.route('/api/clear-cache', methods=['POST'])
def clear_cache():
    """Clear cache"""
    data = request.json
    key = data.get('key')
    
    success = cache.clear(key)
    
    return jsonify({
        'success': success
    })

@app.route('/results')
def results():
    """Render results page"""
    return render_template('results.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
