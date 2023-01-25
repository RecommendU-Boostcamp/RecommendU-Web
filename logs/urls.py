from django.urls import path
from . import views


app_name = 'logs'

urlpatterns = [
    path('answerlog/', views.answerlog, name='answerlog'),
    path('recbuttonlog/', views.recbuttonlog, name='recbuttonlog'),
    path('user_eval/',views.eval_log,name='evallog')
]