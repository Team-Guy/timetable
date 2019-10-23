from schedule.models import Activity, User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# @action(methods=['get'], detail=True)
#     queryuser = User.objects.get(User.email, request.data)
#     queryset = Activity.objects.all(Activity.group, queryuser.group)
#     serializer = AcitivitySerializer(queryset, many=True)
#     return Response(serializer.data)
