# Register your models here.
from django.contrib import admin

from Ara_Ara.models import *

admin.register(Anime)(admin.ModelAdmin)
admin.register(Review)(admin.ModelAdmin)
