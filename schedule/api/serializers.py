from rest_framework import serializers
from schedule.models import Activity

class AcitivitySerializer(serializers.ModelSerializer):
     class Meta:
         model = Activity
         fields = ('title', 'professor', 'location', 'group', 'start_time', 'duration', 'frequency', 'priority', 'type', 'description')
