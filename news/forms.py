from django.forms import ModelForm, BooleanField
from .models import Post


class PostForm(ModelForm):
    check_box = BooleanField(label='Add')

    class Meta:
        model = Post
        fields = ['category_type', 'post_category', 'title', 'text', 'author_us']