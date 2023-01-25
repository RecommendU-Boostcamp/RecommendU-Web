from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from services.models import MajorSmall,Company,JobLarge,Answer
from logs.models import AnswerLog,EvalLog
# Create your models here.


class User(AbstractUser):
    career_type = models.CharField(max_length=10,null=False)
    recommend_cnt = models.IntegerField(default=0)
    major_small = models.ForeignKey(MajorSmall,related_name="users",on_delete=models.SET_NULL,null=True)
    favorite_company = models.ForeignKey(Company,related_name="users",on_delete=models.SET_NULL,null=True)
    interesting_job_large = models.ForeignKey(JobLarge,related_name="users",on_delete=models.SET_NULL,null=True)
    answer_log = models.ManyToManyField(Answer,related_name='recorded_user',through=AnswerLog)
    answer_eval = models.ManyToManyField(Answer,related_name="eval_answers",through=EvalLog)
    answer_scrap = models.ManyToManyField(Answer,related_name="scrap_users")