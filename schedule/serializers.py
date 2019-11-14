from rest_framework import serializers
from . import models


class SchoolActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolActivity
        fields = ("title", "location", "start_time", "day", "duration", "frequency", "priority", "group", "professor")


class ExtraActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExtraActivity
        fields = ('title', 'location', 'start_time', 'day', 'duration', 'frequency', 'priority', 'description')
