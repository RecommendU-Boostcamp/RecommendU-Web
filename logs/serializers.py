from rest_framework import serializers

from .models import RecommendLog, AnswerLog,EvalLog

class EvalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=EvalLog
        fields='__all__'
        
class AnswerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerLog
        fields='__all__'

class RecommendLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=RecommendLog
        fields='__all__'