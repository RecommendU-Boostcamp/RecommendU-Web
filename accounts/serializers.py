from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_list_or_404, get_object_or_404

from services.serializers import MajorSmallSerializer, JobLargeSerializer
from services.models import MajorSmall, JobLarge

# class MyRegisterSerializer(RegisterSerializer):
#     major = serializers.PrimaryKeyRelatedField(queryset=MajorSmall.objects.all())
#     interesting_domain = serializers.PrimaryKeyRelatedField(queryset=JobLarge.objects.all())

#     def perform_create(self, serializer):
#         try:
#             user = serializer.save(self.request)
#             major_id = self.request.data.get('major', None)
#             interesting_domain_id = self.request.data.get('interesting_domain', None)
#             if major_id:
#                 user.major_id = major_id
#             if interesting_domain_id:
#                 user.interesting_domain_id = interesting_domain_id
#             user.save()
            
#         except Exception as e:
#             raise serializers.ValidationError({'error': str(e)})
        
#         return user

# class User(AbstractUser):
#     user_id = models.CharField(null=False,primary_key=True,max_length=15)
#     career_type = models.CharField(max_length=10,null=False)
#     recommend_cnt = models.IntegerField(default=0)
#     major_small = models.ForeignKey(MajorSmall,related_name="users",on_delete=models.SET_NULL,null=True)
#     favorite_company = models.ForeignKey(Company,related_name="users",on_delete=models.SET_NULL,null=True)
#     interesting_job_large = models.ForeignKey(JobLarge,related_name="users",on_delete=models.SET_NULL,null=True)
#     answer_log = models.ManyToManyField(Answer,related_name='recorded_user',through=AnswerLog)