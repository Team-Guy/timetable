from schedule.models import Activity, User
from .serializers import AcitivitySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class ActivitesViewSet(viewsets.ViewSet):

   def list(self, request):
       queryset = Activity.objects.all()
       serializer = AcitivitySerializer(queryset, many=True)
       return Response(serializer.data)

   @action(methods=['get'], detail=True)
   def userActivities(self, request):
       queryset = User.objects.first(email=request.data)
       queryset2 = Activity.objects.all(group=queryset.group)
       serializer = AcitivitySerializer(queryset2, many=True)
       return Response(serializer.data)






