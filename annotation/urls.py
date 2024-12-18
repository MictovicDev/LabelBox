from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.create_project, name='project'),
    path('<int:pk>/', views.get_detail, name='project-detail'),
    path('<int:pk>/<int:index>/', views.save_and_next, name='save_and_next'),
    path('back/<int:pk>/<int:index>/', views.back, name='back'),
]