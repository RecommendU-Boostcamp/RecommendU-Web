from django.db import models
from django.contrib.auth.models import AbstractUser
from services.models import MajorSmall,Company,JobLarge,Answer
from logs.models import AnswerLog
# Create your models here.

class User(AbstractUser):
    user_id = models.CharField(null=False,primary_key=True,max_length=15)
    career_type = models.CharField(max_length=10,null=False)
    recommend_cnt = models.IntegerField(default=0)
    major_small = models.ForeignKey(MajorSmall,related_name="users",on_delete=models.SET_NULL,null=True)
    favorite_company = models.ForeignKey(Company,related_name="users",on_delete=models.SET_NULL,null=True)
    interesting_job_large = models.ForeignKey(JobLarge,related_name="users",on_delete=models.SET_NULL,null=True)
    answer_log = models.ManyToManyField(Answer,related_name='recorded_user',through=AnswerLog)