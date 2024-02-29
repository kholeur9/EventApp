import locale
from django.contrib.auth.models import User
from django.db import models
from organisator.models import Organisation

class Categorie(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()

  class Meta:
    ordering = ['name',]
    verbose_name_plural = "Catégories"

  def __str__(self):
    return self.name

class Event(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  start_datetime = models.DateTimeField()
  end_datetime = models.DateTimeField()
  location = models.CharField(max_length=100)
  image = models.ImageField(upload_to='event_images')
  category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='events')
  capacity = models.PositiveIntegerField()
  organisator = models.ForeignKey(Organisation, on_delete=models.CASCADE)
  is_sold_out = models.BooleanField(default=False)
  status = models.CharField(max_length=20, choices=[('confirmé', 'Confirmé'), ('annuler', 'Annuler'), ('en_cours', 'En cours'), ('termine', 'Terminé')])
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-start_datetime',]
    verbose_name_plural = "Evenements"

  def __str__(self):
    return self.title

class Favoris(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='favoris')
  add_time = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-add_time']
    unique_together = ('user', 'event',)

  def __str__(self):
    return self.user.username + " favoris " + self.event.title