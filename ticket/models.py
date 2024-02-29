from django.db import models
from evenement.models import Event
import uuid

class Ticket(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
  price = models.IntegerField(default=0)
  is_sold = models.BooleanField(default=False)
  date_dold = models.DateField(auto_now_add=True)

  class Meta:
    ordering = ['-date_dold']
    verbose_name_plural = "billets"

  def __str__(self):
    return f"{self.event.title} - {self.price}Fcfa"