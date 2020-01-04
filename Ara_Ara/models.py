from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Anime(models.Model):
    name = models.CharField(max_length=100)
    synopsis = models.TextField(default="")
    poster = models.ImageField(upload_to=f'Ara_Ara/anime/', null=True)
    status = models.CharField(max_length=1,
                              choices=(('a', "airing"), ('n', "not yet aired"), ('f', "finished airing")), default='n')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    season = models.CharField(max_length=2,
                              choices=(('sp', "spring"), ('sm', "summer"), ('fa', "fall"), ('wn', "winter")), null=True)
    total_eps = models.IntegerField(default=12)
    aired_eps = models.IntegerField(default=0)
    rating = models.CharField(max_length=4,
                              choices=(
                                  ('g', "General Audiences"),
                                  ('pg', "Parental Guidance Suggested"),
                                  ('pg13', "Parents Strongly Cautioned"),
                                  ('r', " Inappropriate for Audiences under 17"),
                                  ('nc17', "No One 17 and Under Admitted"),
                              ), default='g')
    opening_theme = models.CharField(max_length=50, null=True)
    ending_theme = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'Anime'


class Review(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(default="")

    class Meta:
        db_table = 'Review'
