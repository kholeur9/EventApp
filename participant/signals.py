from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Participant
from social_django.models import UserSocialAuth
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_participant(sender, instance, created, **kwargs):
  if created:
    logger.info(f'User {instance.username} created')
    try:
      user_social = UserSocialAuth.objects.filter(user=instance, provider='google-oauth2').exists()
      logger.info(f'User has a google account')
      Participant.objects.create(user=instance, email=instance.email)
      logger.info(f'Participant created.')
    except UserSocialAuth.DoesNotExist:
      logger.warning(f'UserSocialAuth for google not found')

@receiver(post_save, sender=User)
def save_participant(sender, instance, **kwargs):
  if hasattr(instance, 'participant'):
    instance.participant.save()