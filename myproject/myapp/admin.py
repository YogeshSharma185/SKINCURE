import uuid
from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Doctor, UserProfile, Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "status", "date", "time")
    readonly_fields = ("meeting_link",)

    def save_model(self, request, obj, form, change):

        # 👉 Get old status (to avoid resending mails unnecessarily)
        old_status = None
        if change:
            old_status = Appointment.objects.get(pk=obj.pk).status

        # ------------------ APPROVED ------------------
        if obj.status == "Approved" and old_status != "Approved":

            # Generate meeting ID if not exists
            if not obj.meeting_id:
                obj.meeting_id = uuid.uuid4().hex[:12]

            base_meet_url = f"https://meet.jit.si/{obj.meeting_id}"
            obj.meeting_link = base_meet_url

            super().save_model(request, obj, form, change)

            doctor_link = f"{base_meet_url}?host=1"
            patient_link = base_meet_url

            # ✉️ Patient Mail
            patient_email_text = f"""
Dear {obj.patient.username},

Your appointment has been APPROVED ✅

Doctor: {obj.doctor.name}
Date: {obj.date}
Time: {obj.time}

Join the meeting using the link below:
{patient_link}

# Meeting ID: {obj.meeting_id}

Please wait until the doctor joins the meeting.

Regards,
SkinCure Team
"""

            # ✉️ Doctor Mail
            doctor_email_text = f"""
Dear {obj.doctor.name},

You have APPROVED an appointment ✅

Patient: {obj.patient.username}
Date: {obj.date}
Time: {obj.time}

Host the meeting using the link below:
{doctor_link}

Meeting ID: {obj.meeting_id}

You will be the host of this session.

Regards,
SkinCure Team
"""

            send_mail(
                "SkinCure | Appointment Approved",
                patient_email_text,
                settings.EMAIL_HOST_USER,
                [obj.patient.email],
            )

            send_mail(
                "SkinCure | Appointment Approved (Doctor)",
                doctor_email_text,
                settings.EMAIL_HOST_USER,
                [obj.doctor.email],
            )

        # ------------------ REJECTED ------------------
        elif obj.status == "Rejected" and old_status != "Rejected":

            super().save_model(request, obj, form, change)

            patient_email_text = f"""
Dear {obj.patient.username},

We regret to inform you that your appointment has been REJECTED ❌

Doctor: {obj.doctor.name}
Date: {obj.date}
Time: {obj.time}

You may book another appointment at your convenience.

Regards,
SkinCure Team
"""

            doctor_email_text = f"""
Dear {obj.doctor.name},

You have REJECTED an appointment ❌

Patient: {obj.patient.username}
Date: {obj.date}
Time: {obj.time}

No further action is required.

Regards,
SkinCure Team
"""

            send_mail(
                "SkinCure | Appointment Rejected",
                patient_email_text,
                settings.EMAIL_HOST_USER,
                [obj.patient.email],
            )

            send_mail(
                "SkinCure | Appointment Rejected (Doctor)",
                doctor_email_text,
                settings.EMAIL_HOST_USER,
                [obj.doctor.email],
            )

        # ------------------ PENDING ------------------
        elif obj.status == "Pending" and old_status != "Pending":

            super().save_model(request, obj, form, change)

            patient_email_text = f"""
Dear {obj.patient.username},

Your appointment request has been submitted ⏳

Doctor: {obj.doctor.name}
Date: {obj.date}
Time: {obj.time}

Please wait while the doctor reviews your request.

Regards,
SkinCure Team
"""

            send_mail(
                "SkinCure | Appointment Pending",
                patient_email_text,
                settings.EMAIL_HOST_USER,
                [obj.patient.email],
            )

        else:
            super().save_model(request, obj, form, change)


admin.site.register(Doctor)
admin.site.register(UserProfile)
admin.site.register(Appointment, AppointmentAdmin)
