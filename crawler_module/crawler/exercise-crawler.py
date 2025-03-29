import json
import asyncio
from typing import Dict, List, Optional, Union
from crawl4ai import AsyncWebCrawler, arun
from bs4 import BeautifulSoup
import logging

from .parser import ExerciseParser

logger = logging.getLogger(__name__)

class ExerciseCrawler:
    """Crawler for exercise data from Virtuagym"""
    
    BASE_URL = "https://exercises.virtuagym.com"
    
    def __init__(self, headless: bool = True, js_render: bool = True, bypass_cache: bool = False):
        """
        Initialize the crawler
        
        Args:
            headless: Run browser in headless mode
            js_render: Enable JavaScript rendering
            bypass_cache: Bypass cache when crawling
        """
        self.crawler = AsyncWebCrawler(
            headless=headless,
            js_render=js_render
        )
        self.bypass_cache = bypass_cache
        self.parser = ExerciseParser()
        
    async def crawl_main_page(self) -> Dict:
        """Crawl the main page to get exercise categories"""
        try:
            result = await self.crawler.run(
                url=self.BASE_URL,
                bypass_cache=self.bypass_cache
            )
            
            categories = self.parser.extract_categories(result.get('html', ''))
            return {
                'success': True,
                'categories': categories,
                'count': len(categories)
            }
        except Exception as e:
            logger.error(f"Error crawling main page: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def crawl_category(self, category_url: str) -> Dict:
        """
        Crawl a specific exercise category
        
        Args:
            category_url: URL of the category to crawl
            
        Returns:
            Dictionary containing exercises in the category
        """
        full_url = f"{self.BASE_URL}{category_url}" if not category_url.startswith("http") else category_url
        
        try:
            result = await self.crawler.run(
                url=full_url,
                bypass_cache=self.bypass_cache
            )
            
            exercises = self.parser.extract_exercises(result.get('html', ''))
            return {
                'success': True,
                'category_url': category_url,
                'exercises': exercises,
                'count': len(exercises)
            }
        except Exception as e:
            logger.error(f"Error crawling category {category_url}: {str(e)}")
            return {
                'success': False,
                'category_url': category_url,
                'error': str(e)
            }
    
    async def crawl_exercise(self, exercise_url: str) -> Dict:
        """
        Crawl a specific exercise page
        
        Args:
            exercise_url: URL of the exercise to crawl
            
        Returns:
            Dictionary containing exercise details
        """
        full_url = f"{self.BASE_URL}{exercise_url}" if not exercise_url.startswith("http") else exercise_url
        
        try:
            result = await self.crawler.run(
                url=full_url,
                bypass_cache=self.bypass_cache
            )
            
            exercise_details = self.parser.extract_exercise_details(result.get('html', ''))
            return {
                'success': True,
                'exercise_url': exercise_url,
                'details': exercise_details
            }
        except Exception as e:
            logger.error(f"Error crawling exercise {exercise_url}: {str(e)}")
            return {
                'success': False,
                'exercise_url': exercise_url,
                'error': str(e)
            }
    
    async def crawl_all_categories(self) -> Dict:
        """Crawl all exercise categories"""
        main_page_result = await self.crawl_main_page()
        
        if not main_page_result['success']:
            return main_page_result
        
        categories = main_page_result['categories']
        category_results = []
        
        # Process categories in parallel (with a limit to avoid overwhelming the server)
        tasks = []
        for category in categories[:5]:  # Limit to 5 categories for demo purposes
            tasks.append(self.crawl_category(category['url']))
        
        category_results = await asyncio.gather(*tasks)
        
        return {
            'success': True,
            'categories': categories,
            'category_results': category_results
        }
    
    def run_crawler(self, task: str = 'main', url: Optional[str] = None) -> Dict:
        """
        Run the crawler for different tasks
        
        Args:
            task: Type of crawl ('main', 'category', 'exercise', 'all')
            url: URL for category or exercise if needed
            
        Returns:
            Crawling results
        """
        if task == 'main':
            return arun(self.crawl_main_page(), magic=False)
        elif task == 'category' and url:
            return arun(self.crawl_category(url), magic=False)
        elif task == 'exercise' and url:
            return arun(self.crawl_exercise(url), magic=False)
        elif task == 'all':
            return arun(self.crawl_all_categories(), magic=False)
        else:
            return {
                'success': False,
                'error': 'Invalid task or missing URL parameter'
            }
