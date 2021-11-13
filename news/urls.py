from django.urls import path
from .views import NewsList, NewsDetail, Search, NewsCreate, NewsUpdate, NewsDelete, CategoryView
from .views import subscribe_me, unsubscribe_me
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news'),
    path('<int:pk>', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),
    path('search/', Search.as_view(), name='news_search'),
    path('add/', NewsCreate.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('categories/', cache_page(60*5)(CategoryView.as_view()), name='subscribes'),
    path('categories/<int:cat_id>/subscribes/', subscribe_me, name='subscribes'),
    path('categories/<int:cat_id>/unsubscribes/', unsubscribe_me, name='subscribes'),
]

