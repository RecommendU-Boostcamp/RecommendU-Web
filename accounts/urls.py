from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/',views.mypage,name='mypage'),
    path('myscrap/',views.myscrap,name='myscrap'),
    path('myinfo/',views.myinfo,name='myinfo'),
    path('update/',views.update,name='update'),
    path('namecheck/', views.namecheck, name='namecheck'),
    path('total/',views.totaluser,name='total'),
    path('change_password/', views.change_password, name='change_password'),
]