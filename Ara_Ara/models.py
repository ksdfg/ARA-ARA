from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Anime(models.Model):
    name = models.CharField(max_length=100)
    total_eps = models.IntegerField()
    aired_eps = models.IntegerField(null=True)
    status = models.CharField(max_length=1,
                              choices=(('a', "airing"), ('n', "not yet aired"), ('f', "finished airing")), default='n')

    class Meta:
        db_table = 'Anime'


class Review(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(default="")

    class Meta:
        db_table = 'Review'
