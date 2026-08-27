from .models import ProfessionalProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_professional_profile(sender, instance, created, **kwargs):
    if created and instance.role=='professional':
        ProfessionalProfile.objects.create(user=instance)
