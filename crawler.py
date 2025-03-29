from crawl4ai import AsyncCrawler
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
from fastapi import FastAPI, BackgroundTasks
from typing import List, Optional
import uvicorn

app = FastAPI(title="Exercise Crawler API")

class ExerciseCrawler(AsyncCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bodybuilding.com/exercises"
        self.exercises = []

    async def parse_exercise(self, response):
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

    async def crawl(self):
        """شروع خزش از صفحه اصلی"""
        # دریافت لیست تمرین‌ها
        response = await self.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        exercise_links = soup.select('a.ExerciseCard')

        # خزش هر تمرین
        for link in tqdm(exercise_links, desc="Crawling exercises"):
            exercise_url = link['href']
            await self.get(exercise_url, callback=self.parse_exercise)

        # ذخیره نتایج
        await self.save_results()

    async def save_results(self):
        """ذخیره نتایج در فایل JSON"""
        if not os.path.exists('dist'):
            os.makedirs('dist')
            
        with open('dist/exercises.json', 'w', encoding='utf-8') as f:
            json.dump(self.exercises, f, ensure_ascii=False, indent=2)

crawler = ExerciseCrawler()

@app.get("/")
async def read_root():
    return {"message": "Exercise Crawler API"}

@app.post("/crawl")
async def start_crawl(background_tasks: BackgroundTasks):
    """شروع عملیات خزش در پس‌زمینه"""
    background_tasks.add_task(crawler.crawl)
    return {"message": "Crawling started in background"}

@app.get("/exercises")
async def get_exercises():
    """دریافت لیست تمرین‌های ذخیره شده"""
    try:
        with open('dist/exercises.json', 'r', encoding='utf-8') as f:
            exercises = json.load(f)
        return exercises
    except FileNotFoundError:
        return {"message": "No exercises found. Start crawling first."}

if __name__ == "__main__":
    uvicorn.run("crawler:app", host="0.0.0.0", port=8000, reload=True) 