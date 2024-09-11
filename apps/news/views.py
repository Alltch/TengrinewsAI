from apps.news.parse import NewsParser
from django.http import HttpResponse

def start_scraper(request):
    parser = NewsParser(url='https://tengrinews.kz/')
    parser.processing()
    return HttpResponse("Scraping completed successfully!")
