from django.db import models
from services.models import Answer,RecommendType,JobSmall,Company,QuestionType
from django.conf import settings
# Create your models here.

class AnswerLog(models.Model):
    answer_log_id = models.BigAutoField(primary_key=True,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
    rectype = models.ForeignKey(RecommendType,on_delete=models.SET_NULL,null=True)

class RecommendLog(models.Model):
    rec_log_id = models.BigAutoField(primary_key=True,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="rec_logs",on_delete=models.CASCADE,null=False)
    company = models.ForeignKey(Company,related_name="rec_logs",on_delete=models.SET_NULL,null=True)
    job_small = models.ForeignKey(JobSmall,related_name="rec_logs",on_delete=models.SET_NULL,null=True)
    question_type = models.ForeignKey(QuestionType,related_name="rec_logs",on_delete=models.SET_NULL,null=True)