from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    id_posts = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_group = models.CharField(max_length=10)
    date_post = models.DateTimeField()
    url_post = models.TextField()
    url_img = models.TextField()
    text_post = models.TextField()
    c_like = models.IntegerField(max_length=10)
    c_comments = models.IntegerField(max_length=10)
    c_views = models.IntegerField(max_length=10)
    c_reposts = models.IntegerField(max_length=10)



# python manage.py makemigrations app
#python manage.py migrate app
