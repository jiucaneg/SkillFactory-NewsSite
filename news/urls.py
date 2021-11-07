from django.urls import path
from .views import NewsList, NewsDetail, Search, NewsCreate, NewsUpdate, NewsDelete, CategoryView
from .views import subscribe_me, unsubscribe_me

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', Search.as_view(), name='news_search'),
    path('add/', NewsCreate.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('categories/', CategoryView.as_view(), name='subscribes'),
    path('categories/<int:cat_id>/subscribes/', subscribe_me, name='subscribes'),
    path('categories/<int:cat_id>/unsubscribes/', unsubscribe_me, name='subscribes'),
]

