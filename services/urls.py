from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('init/', views.db_first),
    path('init2/', views.docu_answer_init),
]