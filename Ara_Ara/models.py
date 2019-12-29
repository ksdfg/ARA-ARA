from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'User'


class Anime(models.Model):
    name = models.CharField(max_length=100)
    total_eps = models.IntegerField()
    aired_eps = models.IntegerField(null=True)
    status = models.CharField(max_length=1,
                              choices=(('a', "airing"), ('n', "not yet aired"), ('f', "finished airing")))

    class Meta:
        db_table = 'Anime'
