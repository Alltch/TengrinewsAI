from datetime import datetime
import json

import requests
from bs4 import BeautifulSoup


class News_parser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36'
        }

    def get_html(self) -> str:
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            print(f'Error pars-log: {response.status_code}')
            return None
        return response.text
    
    def process_time(self, time_str: str):
        clean_time_str = time_str.strip()

        if "Сегодня" in clean_time_str:
            clean_time_str = clean_time_str.replace("Сегодня | ", "").strip()
            base_date = datetime.now()
        elif "Вчера" in clean_time_str:
            clean_time_str = clean_time_str.replace("Вчера | ", "").strip()
            base_date = datetime.now().replace(day=datetime.now().day - 1)
        else:
            return None
        
        return base_date
    
    def processing(self):
        html = self.get_html()
        if not html:
            print('Error pars-log: html is None')
            return None
        
        output = []

        soup = BeautifulSoup(html, features='lxml')
        news = soup.find('div', class_='tab-content').find_all('div', class_='main-news_top_item')


        for new in news:
            new:BeautifulSoup
            if new.find('div', class_='main-news_top_item_meta').find('span', class_='subproject'):
                continue
            else:
                title = new.find('span', class_='main-news_top_item_title').find('a').get_text(strip=True)
                date = new.find('div', class_='main-news_top_item_meta').find('time').get_text(strip=True)
                # if "Сегодня" in date:
                #     date = date.replace("Сегодня | ", "").strip()
                #     # base_date = ...
                # elif "Вчера" in date:
                #     date = date.replace("Вчера | ", "").strip()
                #     # base_date = ...
                # else:
                #     return None
            
            output.append({
                'title': title,
                'date': date
            })

        
        return output
    
    

    
    def run_parse(self):
        output = self.processing()
        if not output:
            print('Error pars-log: output is None')
            return None
        
        return output
    

news = News_parser('https://tengrinews.kz/')

with open('news.json', 'w', encoding='utf-8') as file:
    json.dump(news.run_parse(), file, indent=4, ensure_ascii=False)