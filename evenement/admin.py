from django.contrib import admin
from .models import Categorie, Event, Favoris

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Event)
admin.site.register(Favoris)