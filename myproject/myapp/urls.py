from django.urls import path
from . import views
# from django.urls import path
from django.contrib.auth import views as auth_views
# from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("disease/", views.disease, name="disease"),
    path("prediction/", views.prediction_page, name="prediction"),
    path("predict/", views.predict, name="predict"),
    path("contact/", views.contact, name="contact"),
    path('result/<str:disease>/', views.result_page, name='result_page'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path("book/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("appointment_success/", views.appointment_success, name="appointment_success"),
    path("profile/", views.profile_page, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("forgot/", auth_views.PasswordResetView.as_view(template_name="forgot.html"), name="forgot"),
    path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html",
        success_url=reverse_lazy("login")
    ),
    name="password_reset_confirm",
),
    # path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",success_url="/login/"),name="password_reset_confirm",),
]
