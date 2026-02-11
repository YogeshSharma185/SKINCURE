from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M','Male'),('F','Female')])
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.user.email

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    experience = models.IntegerField()
    rating_sum = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    email = models.EmailField(null=True, blank=True)
    def avg_rating(self):
        if self.rating_count == 0:
            return 0
        return round(self.rating_sum / self.rating_count, 1)

    def total_patients(self):
        return Appointment.objects.filter(
            doctor=self,
            status="Approved"
        ).count()

    def __str__(self):
        return self.name
class Appointment(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    problem = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    meeting_id = models.CharField(max_length=200, blank=True, null=True)
    meeting_password = models.CharField(max_length=50, blank=True, null=True)
    meeting_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} → {self.doctor.name}"