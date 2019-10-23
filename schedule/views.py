from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from schedule.api.serializers import ActivitySerializer
from schedule.models import Activity, User


@api_view(['GET'])
def list_activities(request):
    query_set = Activity.objects.all()
    serializer = ActivitySerializer(query_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_activities(request):
    query_user = User.objects.get(User.email, request.data)
    queryset = Activity.objects.filter(Activity.group, query_user.group)
    serializer = ActivitySerializer(queryset, many=True)
    return Response(serializer.data)
