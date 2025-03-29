from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

class ExerciseParser:
    """Parser for exercise data from Virtuagym"""
    
    def extract_categories(self, html: str) -> List[Dict]:
        """
        Extract exercise categories from HTML
        
        Args:
            html: HTML content of the main page
            
        Returns:
            List of category dictionaries with name and URL
        """
        soup = BeautifulSoup(html, 'html.parser')
        categories = []
        
        try:
            category_section = soup.select('.category-list')
            if not category_section:
                logger.warning("Category list section not found")
                return categories
                
            category_links = soup.select('.category-list a')
            
            for link in category_links:
                name = link.get_text(strip=True)
                url = link.get('href')
                if name and url:
                    categories.append({
                        'name': name,
                        'url': url
                    })
            
            # If not found with the expected class, try a more general approach
            if not categories:
                logger.info("Trying alternative category extraction method")
                for link in soup.find_all('a'):
                    if '/exercises/' in link.get('href', ''):
                        name = link.get_text(strip=True)
                        url = link.get('href')
                        if name and url:
                            categories.append({
                                'name': name,
                                'url': url
                            })
            
        except Exception as e:
            logger.error(f"Error extracting categories: {str(e)}")
        
        return categories
    
    def extract_exercises(self, html: str) -> List[Dict]:
        """
        Extract exercises from a category page
        
        Args:
            html: HTML content of the category page
            
        Returns:
            List of exercise dictionaries with name, URL, and image
        """
        soup = BeautifulSoup(html, 'html.parser')
        exercises = []
        
        try:
            exercise_items = soup.select('.exercise-item, .exercise-block')
            
            for item in exercise_items:
                exercise = {}
                
                # Try to get name and URL
                link_elem = item.select_one('a')
                if link_elem:
                    exercise['name'] = link_elem.get_text(strip=True)
                    exercise['url'] = link_elem.get('href')
                
                # Try to get image
                img_elem = item.select_one('img')
                if img_elem:
                    exercise['image'] = img_elem.get('src')
                
                # Try to get description
                desc_elem = item.select_one('.exercise-description')
                if desc_elem:
                    exercise['description'] = desc_elem.get_text(strip=True)
                
                if exercise.get('name') and exercise.get('url'):
                    exercises.append(exercise)
            
            # If not found with expected classes, try a more general approach
            if not exercises:
                logger.info("Trying alternative exercise extraction method")
                for link in soup.find_all('a'):
                    if '/exercise/' in link.get('href', ''):
                        name = link.get_text(strip=True)
                        url = link.get('href')
                        
                        # Find closest image
                        img = link.find('img') or link.find_previous('img') or link.find_next('img')
                        image_url = img.get('src') if img else None
                        
                        if name and url:
                            exercises.append({
                                'name': name,
                                'url': url,
                                'image': image_url
                            })
                
        except Exception as e:
            logger.error(f"Error extracting exercises: {str(e)}")
        
        return exercises
    
    def extract_exercise_details(self, html: str) -> Dict:
        """
        Extract details from an exercise page
        
        Args:
            html: HTML content of the exercise page
            
        Returns:
            Dictionary with exercise details
        """
        soup = BeautifulSoup(html, 'html.parser')
        details = {}
        
        try:
            # Extract name
            name_elem = soup.select_one('h1, .exercise-name')
            if name_elem:
                details['name'] = name_elem.get_text(strip=True)
            
            # Extract images
            images = []
            for img in soup.select('.exercise-image img, .exercise-photos img'):
                src = img.get('src')
                if src:
                    images.append(src)
            details['images'] = images
            
            # Extract description
            desc_elem = soup.select_one('.exercise-description, .description')
            if desc_elem:
                details['description'] = desc_elem.get_text(strip=True)
            
            # Extract instructions
            instructions_elem = soup.select_one('.exercise-instructions, .instructions')
            if instructions_elem:
                details['instructions'] = instructions_elem.get_text(strip=True)
            
            # Extract muscles worked
            muscles = []
            muscles_elem = soup.select('.muscle-worked, .muscles-worked')
            for muscle in muscles_elem:
                muscle_name = muscle.get_text(strip=True)
                if muscle_name:
                    muscles.append(muscle_name)
            details['muscles_worked'] = muscles
            
            # Extract difficulty
            difficulty_elem = soup.select_one('.difficulty-level')
            if difficulty_elem:
                details['difficulty'] = difficulty_elem.get_text(strip=True)
            
            # Extract equipment
            equipment_elem = soup.select_one('.equipment-needed')
            if equipment_elem:
                details['equipment'] = equipment_elem.get_text(strip=True)
            
        except Exception as e:
            logger.error(f"Error extracting exercise details: {str(e)}")
        
        return details
