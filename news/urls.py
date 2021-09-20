from django.urls import path
from .views import NewsList, NewsDetail, Search, NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', Search.as_view(), name='news_search'),
    path('add/', NewsCreate.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]

