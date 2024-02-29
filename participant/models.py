from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Participant(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  email = models.EmailField(max_length=100)
  phone = models.CharField(max_length=100, blank=True, null=True)
  address = models.CharField(max_length=100, blank=True, null=True)
  country = models.CharField(max_length=100, blank=True, null=True)
  city = models.CharField(max_length=100, blank=True, null=True)
  date_birth = models.CharField(max_length=100, blank=True, null=True)
  photo = models.ImageField(upload_to='participant/photos', blank=True, null=True)

  USERNAME_FIELD = 'email'

  def __str__(self):
    return self.user.username