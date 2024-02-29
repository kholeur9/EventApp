from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Organisation(models.Model):
  nom = models.CharField(max_length=50)
  description = models.TextField()
  createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organisations_crees', null=True, blank=True)

  def __str__(self):
    return self.nom

class Organisateur(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  nom = models.CharField(max_length=100, blank=False, null=False)
  prenom = models.CharField(max_length=100, blank=False, null=False)
  email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
  telephone = models.CharField(max_length=100, blank=True, null=True)
  adresse = models.CharField(max_length=100, blank=True, null=True)
  pays = models.CharField(max_length=100, blank=True, null=True)
  ville = models.CharField(max_length=100, blank=True, null=True)
  code_postal = models.CharField(max_length=100, blank=True, null=True)
  date_naissance = models.DateField(blank=True, null=True)
  lieu_naissance = models.CharField(max_length=100, blank=True, null=True)
  photo = models.ImageField(upload_to='organisateurs', blank=True)
  organisations_crees = models.ManyToManyField(Organisation, related_name='organisateurs')
  organisations_affiliees = models.ManyToManyField(Organisation, related_name='organisateurs_affiliees')

  USERNAME_FIELD = 'email'

  def __str__(self):
    return f"{self.nom} - {self.prenom}"