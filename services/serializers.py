from rest_framework import serializers
from .models import (
    QuestionType, Company, MajorLarge, MajorSmall,
    JobLarge, JobSmall, RecommendType, SchoolType, 
    Document, Answer, Sample,
)

class QuestionTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionType
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = ('company_id', 'company')
    
    
class MajorSmallSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MajorSmall
        fields = '__all__'  # major_large가 자동으로 serialize되는지 한 번만 확인
        

class MajorLargeSerializer(serializers.ModelSerializer):
    major_smalls = MajorSmallSerializer(many=True, read_only=True)
    
    class Meta:
        model = MajorLarge
        fields = '__all__'


class JobSmallTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSmall
        fields = '__all__'

        
class JobLargeSerializer(serializers.ModelSerializer):
    job_smalls = JobSmallTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobLarge
        fields = '__all__'
        
        
class RecommendTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecommendType
        fields = '__all__'
        
        
class SchoolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionType
        fields = '__all__'
    
    
class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = '__all__'
        
        
class DocumentSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuestionType
        fields = '__all__'
