from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()  # 현재 장고에서 사용하는 유저모델 
        fields = ('career_type', 'major_small', 'interesting_job_large',)


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'career_type', 'major_small', 'interesting_job_large', )