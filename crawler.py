from crawl4ai import Crawler
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm

class ExerciseCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bodybuilding.com/exercises"
        self.exercises = []

    def parse_exercise(self, response):
        """پردازش صفحه هر تمرین"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        exercise = {
            'name': soup.select_one('h1.ExerciseTitle').text.strip(),
            'category': soup.select_one('div.BBCategoryBadge').text.strip(),
            'muscles': [m.text.strip() for m in soup.select('div.ExerciseMuscles span')],
            'equipment': soup.select_one('div.ExerciseEquipment').text.strip(),
            'level': soup.select_one('div.ExerciseLevel').text.strip(),
            'instructions': [i.text.strip() for i in soup.select('ol.ExerciseInstructions li')],
            'images': [img['src'] for img in soup.select('div.ExerciseMedia img')]
        }
        
        self.exercises.append(exercise)
        return exercise

    def crawl(self):
        """شروع خزش از صفحه اصلی"""
        # دریافت لیست تمرین‌ها
        response = self.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        exercise_links = soup.select('a.ExerciseCard')

        # خزش هر تمرین
        for link in tqdm(exercise_links, desc="Crawling exercises"):
            exercise_url = link['href']
            self.get(exercise_url, callback=self.parse_exercise)

        # ذخیره نتایج
        self.save_results()

    def save_results(self):
        """ذخیره نتایج در فایل JSON"""
        if not os.path.exists('dist'):
            os.makedirs('dist')
            
        with open('dist/exercises.json', 'w', encoding='utf-8') as f:
            json.dump(self.exercises, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    crawler = ExerciseCrawler()
    crawler.crawl() 