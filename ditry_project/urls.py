"""ditry_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from feed import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('', views.home, name='home'),
    path('feed/', include('feed.urls')),
    path('admin/', admin.site.urls),
    path('reset-password/',
         auth_views.PasswordResetView.as_view(template_name = "feed/password_reset.html"),
         name="reset_password"),
    path('reset-password-sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="feed/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="feed/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset-password-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name="feed/password_reset_done.html"),
         name="password_reset_complete"),
    path('change-password',
         auth_views.PasswordChangeView.as_view(template_name="feed/password_change.html"),
         name="password_change"),
    path('change-password-done',
         auth_views.PasswordChangeDoneView.as_view(template_name="feed/password_reset_done.html"),
         name='password_change_done')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
