import requests
from bs4 import BeautifulSoup
from datetime import datetime
from apps.news.models import NewsModel


class NewsParser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36 Edg/128.0.0.0'
        }
    
    def get_html(self):
        response = requests.get(url=self.url, headers=self.headers)
        if response.status_code != 200:
            print(f"Error pars-log: {response.status_code}")
            return None
        return response.text
    
    def processing(self):
        html = self.get_html()
        if not html:
            print('Error pars-log: html is None')
            return None

        output = []

        soup = BeautifulSoup(html, features='lxml')
        news = soup.find('div', class_='tab-content').find_all('div', class_='main-news_top_item')

        for new in news:
            new: BeautifulSoup
            if new.find('div', class_='main-news_top_item_meta').find('span', class_='subproject'):
                continue
            else:
                title = new.find('span', class_='main-news_top_item_title').find('a').get_text(strip=True)
                time_str = new.find('div', class_='main-news_top_item_meta').find('time').get_text(strip=True)
                
                # Парсинг только времени (удаляем "Сегодня |")
                news_time = self.parse_time(time_str)
                if news_time:
                    news_date = datetime.now().replace(hour=news_time.hour, minute=news_time.minute, second=0)

                    # Добавляем данные в список
                    output.append({
                        'title': title,
                        'news_date': news_date
                    })

        # Сохранение данных в базу
        self.save_to_db(output)
        return output

    def parse_time(self, time_str):
        clean_time_str = time_str.strip()

        # Обработка строк, которые начинаются с "Сегодня |" или "Вчера |"
        if "Сегодня" in clean_time_str:
            clean_time_str = clean_time_str.replace("Сегодня |", "").strip()
            base_date = datetime.now()
        elif "Вчера" in clean_time_str:
            clean_time_str = clean_time_str.replace("Вчера |", "").strip()
            base_date = datetime.now().replace(day=datetime.now().day - 1)
        else:
            # Обрабатываем время без указания "Сегодня" или "Вчера"
            return None

        try:
            # Парсим время
            time_part = datetime.strptime(clean_time_str, '%H:%M').time()
            # Возвращаем полную дату с установленным временем
            return base_date.replace(hour=time_part.hour, minute=time_part.minute, second=0)
        except ValueError as e:
            print(f"Time parsing error: {e}")
            return None

    def save_to_db(self, news_data):
        # Сохранение каждой новости в базу данных
        for item in news_data:
            news_obj, created = NewsModel.objects.get_or_create(
                title=item['title'],
                defaults={'news_date': item['news_date']}
            )
            if created:
                print(f"News '{item['title']}' saved successfully.")
            else:
                print(f"News '{item['title']}' already exists in the database.")

