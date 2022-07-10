from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models here.

it = 'IT'
sport = 'SP'
medicine = 'MED'
culture = 'CUL'

article = 'A'
news = 'N'

TAG_LIST = [
    (it, 'Технологии'),
    (sport, 'Спорт'),
    (medicine, 'Медицина'),
    (culture, 'Культура')
]

POST_LIST = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        a = self.post_set.all().aggregate(Sum('rating'))
        b = self.user.comment_set.all().aggregate(Sum('rating'))
        c = self.post_set.all().aggregate(Sum('comment__rating'))
        d = a['rating__sum'] * 3 + b['rating__sum'] + c['comment__rating__sum']
        self.rating = d
        self.save()
        return d


class Category(models.Model):
    name = models.CharField(max_length=3, unique=True, choices=TAG_LIST)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.CharField(max_length=3, choices=POST_LIST)
    title = models.CharField(max_length=255)
    content = models.TextField(default='SomeText...')
    rating = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + '...'
        else:
            return len(self.content)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='SomeText...')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
