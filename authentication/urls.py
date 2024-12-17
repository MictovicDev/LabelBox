from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('', views.home, name="home")
    
]
