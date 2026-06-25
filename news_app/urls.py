from django.urls import path
from .views import admin_page_view, news_list, news_detail, HomePageView, ContactPageView, categoryPageView, singlePageView, \
    NewsCreateView, admin_page_view, SearchResultsView, NewsDeleteView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('news/', news_list, name='all_news_list'),
    path('category/', categoryPageView, name='category_page'),
    path('news/<int:id>/', news_detail, name='news_detail'),
    path('single/', singlePageView, name='single_page'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('admin_page/', admin_page_view, name='admin_page'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    # path('news/create/', news_create, name='news_create'),
]
