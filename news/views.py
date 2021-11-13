from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.cache import cache  # импортируем наш кэш

from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter


# Create your views here.


class NewsList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsDetail(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object()
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-date_creation']
    paginate_by = 2  # поставим постраничный вывод в 10 элементов

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя
        # метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш
        # фильтр в контекст
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news_add.html'
    form_class = PostForm
    success_url = '/news/'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news_add.html'
    form_class = PostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.change_post',)
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryView(ListView):
    model = Category
    template_name = 'subscribes.html'
    context_object_name = 'category'
    queryset = Category.objects.all()
    paginate_by = 10


@login_required
@cache_page(60 * 5)
def subscribe_me(request, cat_id):
    user = request.user
    category = Category.objects.get(pk=cat_id)
    if request.user not in category.subscribers.all():
        category.subscribers.add(user)
    return redirect('/news/categories/')


@login_required
@cache_page(60 * 5)
def unsubscribe_me(request, cat_id):
    user = request.user
    category = Category.objects.get(pk=cat_id)
    if request.user in category.subscribers.all():
        category.subscribers.remove(user)
    return redirect('/news/categories/')
