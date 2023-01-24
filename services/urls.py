from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('init/', views.db_first),
    # path('init2/', views.docu_answer_init),
    path('main/', views.main, name='main'),
    # path('search/', views.search_company),
    path('answers/', views.answer_recommend, name='answer_recommend'),  # POST : 프론트에서 유저정보/질문맥락 받아서 inference 진행 후 자소서 담아서 보내주기  => asnwer serializer
]