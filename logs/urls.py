from django.urls import path
from . import views


app_name = 'logs'

urlpatterns = [
    path('answerlog/', views.answerlog),
    path('recbuttonlog/', views.recbuttonlog),
]