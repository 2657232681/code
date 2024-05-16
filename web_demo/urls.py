from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views, nets

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    path("nets", nets.nets, name="nets"),
    path("changepwd", views.changepwd),

    path('login/',
         views.login_user,
         name='login'),
    path("ocr_log", views.ocr_log, name='ocr_log'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('admin/', admin.site.urls),
]
