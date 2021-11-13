from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.author_user)

    def update_rating(self):
        post_rat = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_rat = 0
        p_rat += post_rat.get('postRating')

        comment_rat = self.author_user.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_rat = 0
        c_rat += comment_rat.get('commentRating')

        self.rating_author = p_rat * 3 + c_rat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    author_us = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='news',)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    date_creation = models.DateTimeField(auto_now_add=True)
    post_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news',)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.title)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    class Meta:
        ordering = ['-date_creation']


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        try:
            return self.comment_post.author.author_user.username
        except:
            return self.comment_user.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()