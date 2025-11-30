from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Denuncia
import requests
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Denuncia)
def track_previous_status(sender, instance, **kwargs):
    """
    Track the previous status before saving to detect changes.
    """
    if instance.pk:
        try:
            previous_instance = Denuncia.objects.get(pk=instance.pk)
            instance._previous_status = previous_instance.status
        except Denuncia.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None

@receiver(post_save, sender=Denuncia)
def send_status_notification(sender, instance, created, **kwargs):
    """
    Send an email notification if the status has changed.
    """
    if created:
        return

    previous_status = getattr(instance, '_previous_status', None)
    current_status = instance.status

    if previous_status and previous_status != current_status:
        logger.info(f"Status changed for Denuncia {instance.id}: {previous_status} -> {current_status}")
        
        try:
            user_email = instance.user.email
            user_name = instance.user.first_name or "Usuario"
            
            subject = f"Actualización de Denuncia: {current_status}"
            message = (
                f"Hola {user_name},\n\n"
                f"El estado de tu denuncia (ID: {instance.id}) ha cambiado.\n"
                f"Estado anterior: {previous_status}\n"
                f"Nuevo estado: {current_status}\n\n"
                f"Atentamente,\nDenuncias Policiales"
            )

            # Send to Notification Service
            # Using the container name 'notification-service' as hostname
            notification_url = "http://notification-service:8000/send-email/"
            payload = {
                "email": user_email,
                "subject": subject,
                "message": message
            }
            
            # Use a short timeout to not block the save process too long
            response = requests.post(notification_url, json=payload, timeout=5)
            
            if response.status_code == 200:
                logger.info(f"Notification sent successfully for Denuncia {instance.id}")
            else:
                logger.error(f"Failed to send notification. Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            logger.error(f"Error connecting to notification service: {str(e)}")
