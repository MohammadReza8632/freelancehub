from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'project', 'freelancer_id', 'cover_letter', 'status', 'created_at')
        read_only_fields = ('project', 'freelancer_id', 'status', 'created_at')