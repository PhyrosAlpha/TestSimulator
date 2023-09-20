from rest_framework import serializers
from .models import Test, Question, Option

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'