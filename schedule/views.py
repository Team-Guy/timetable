from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view

from schedule.models import UserSchoolActivity, SchoolActivity, ExtraActivity, UserExtraActivity
from schedule.serializers import SchoolActivitySerializer, ExtraActivitySerializer


@api_view(['GET'])
def user_schedule(request, username):
    to_return = get_activities('school', username)
    return JsonResponse(data=to_return)


class SchoolActivityViewset(viewsets.ModelViewSet):
    queryset = SchoolActivity.objects.all()
    serializer_class = SchoolActivitySerializer


class ExtraActivityViewset(viewsets.ModelViewSet):
    queryset = ExtraActivity.objects.all()
    serializer_class = ExtraActivitySerializer


@api_view(['GET'])
def user_extra_schedule(request, username):
    to_return = get_activities('extra', username)
    return JsonResponse(data=to_return)


def get_activities(activity_type: str, username: str):
    odd_days_dict = dict(
        monday=list(),
        tuesday=list(),
        wednesday=list(),
        thursday=list(),
        friday=list()
    )
    even_days_dict = dict(
        monday=list(),
        tuesday=list(),
        wednesday=list(),
        thursday=list(),
        friday=list()
    )
    to_return = {1: odd_days_dict, 2: even_days_dict}
    if activity_type == 'school':
        model = UserSchoolActivity
        to_convert = 'school_activity'
    else:
        to_convert = 'extra_activity'
        model = UserExtraActivity
    school_act_qs = model.objects.filter(user__email=f'{username}@gmail.com')
    for user_activity in school_act_qs:
        activity_dict = model_to_dict(getattr(user_activity, to_convert))
        frequency = activity_dict.pop('frequency')
        day = activity_dict.pop('day').lower()
        if frequency == 'full':
            to_return[1][day].append(activity_dict)
            to_return[2][day].append(activity_dict)
        elif frequency == 'even':
            to_return[2][day].append(activity_dict)
        else:
            to_return[1][day].append(activity_dict)
    return to_return


def index(request):
    return HttpResponse("yay")
