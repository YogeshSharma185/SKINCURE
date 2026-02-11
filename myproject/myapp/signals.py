from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import UserProfile, Appointment, Doctor


# Create user profile automatically
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Send email when appointment is approved
@receiver(post_save, sender=Appointment)
def send_meeting_details(sender, instance, created, **kwargs):
    
    # Only send email when appointment is APPROVED + doctor has set meeting id & password
    if instance.status == "Approved" and instance.meeting_id and instance.meeting_password:

        subject = "Appointment Approved"
        message = f"""
Your appointment with Dr. {instance.doctor.name} has been approved.

Meeting Details:
Meeting ID: {instance.meeting_id}
Password: {instance.meeting_password}

Date: {instance.date}
Time: {instance.time}
"""

        # Send to patient
        if instance.patient.email:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.patient.email],
                fail_silently=False
            )

        # Send to doctor (Doctor model me email field hona chahiye)
        if instance.doctor.email:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.doctor.email],
                fail_silently=False
            )
