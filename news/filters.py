from django_filters import filters, FilterSet
from .models import Post


class PostFilter(FilterSet):
    title = filters.CharFilter(label='Заголовок', lookup_expr='icontains')
    date_creation = filters.DateFilter(label='Дата', lookup_expr='gt')

    class Meta:
        model = Post
        fields = ['title', 'date_creation', 'author_us']
