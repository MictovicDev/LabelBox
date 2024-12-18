from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.create_project, name='project'),
    path('/<int:pk>/', views.get_detail, name='project-detail')
]