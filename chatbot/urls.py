from django.urls import path
from . import views

urlpatterns = [
    path('process_query/', views.process_query, name='process_query'),
    path('', views.chatbot, name='chatbot'),
]