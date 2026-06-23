from .models import News
from datetime import datetime
from .models import Category

def latest_news(request):
    latest_news = News.published.all().order_by("-publish_time")[:10]
    context = {
        "latest_news" : latest_news
    }
    return context


def current_date(request):
    return {'today': datetime.now()}

def footer_data(request):
    return {
        'footer_news': News.published.all().order_by('-publish_time')[:3],
        'footer_categories': Category.objects.all(),
    }