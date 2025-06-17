from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["title", "description", "status", "due_date", "created_at", "owner", "is_overdue"]
        read_only_fields = ["created_at", "owner"]

    def get_is_overdue(self, obj):
        return obj.is_overdue

    def create(self, validated_data):
        return Task.objects.create(**validated_data)


