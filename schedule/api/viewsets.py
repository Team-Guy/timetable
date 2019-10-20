from schedule.models import Activity
from .serializers import AcitivitySerializer
from rest_framework import viewsets

class ActivitesViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = AcitivitySerializer

