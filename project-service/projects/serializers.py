from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'budget', 'duration_days', 'created_at', 'status', 'freelancer_id')
        read_only_fields = ('status', 'freelancer_id')
