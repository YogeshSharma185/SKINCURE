"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from myapp import views   
urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  
    # redirect any request to /accounts/login/ to our custom login
    path("accounts/login/", lambda request: redirect("login")),
    # path('accounts/', include("allauth.urls")),
    path('', include('myapp.urls')),
    # SIGNUP
    path('signup/',views.signup, name='signup'),

    # FORGOT PASSWORD
    path('forgot/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html'
    ), name='forgot'),

    path('forgot/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    # PASSWORD RESET CONFIRM (link from email)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # FINAL COMPLETION PAGE
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
    path("custom_logout/", views.custom_logout_view, name="custom_logout"),
    path("logout/success/", TemplateView.as_view(
        template_name="logout_success.html"), 
        name="logout_success"),

]
