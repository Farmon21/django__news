from django.urls import path
from NewsApp.views import (news_list,
                           homePageView,
                           LocalNewsView,
                           ForeignNewsView,
                           TechnologyNewsView,
                           SportNewsView,
                           news_detail,
                           ContactPageView,
                           NewsUpdateView,
                           NewsDeleteView,
                           NewsCreateView,
                           SearchResultList,
                           )

urlpatterns = [
    path('', homePageView, name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path('news/local-news/', LocalNewsView.as_view(), name="local_news_page"),
    path('news/foreign-news/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('news/technology-news/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('news/sport-news/', SportNewsView.as_view(), name='sport_news_page'),
    path('news/<slug>/', news_detail, name='news_detail_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('news-create/', NewsCreateView.as_view(), name='news_create'),
    path('search-result/', SearchResultList.as_view(), name='search_results'),
]
