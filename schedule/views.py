import json

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view

from authentication.models import LastTimetable
from dbutils.timetable_utils import save_last_timetable, get_differences
from schedule.models import SchoolActivity, ExtraActivity, UserExtraActivity, User
from schedule.models import UserSchoolActivity
from schedule.serializers import SchoolActivitySerializer, ExtraActivitySerializer
from schedule.services import Scheduler
from datetime import datetime


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

    def create(self, request, *args, **kwargs):
        user_name = request.data.pop('username')
        data = request.data
        user = User.objects.get(email=user_name)
        act = ExtraActivity(title=data['title'], location=data['location'], day=data['day'],
                            start_time=datetime.strptime(data['start_time'], '%H:%M:%S').time(),
                            duration=int(data['duration']), frequency=data['frequency'], priority=data['priority'],
                            description=data['description'])
        act.save()
        UserExtraActivity(extra_activity=act, user=user).save()
        return JsonResponse(1)


@api_view(['GET'])
def user_extra_schedule(request, username):
    to_return = get_activities('extra', username)
    return JsonResponse(data=to_return)


def user_full_schedule(username):
    school_act = get_activities('school', username)
    extra_act = get_activities('extra', username)
    return {'school': school_act, 'extra': extra_act}


@api_view(['GET'])
def get_initial_timetable(request, username):
    return JsonResponse(data=user_full_schedule(username))


@api_view(['GET'])
def testalgo(request, username):
    last_timetable = json.loads(
        LastTimetable.objects.get(user=User.objects.get(email=f'{username}@gmail.com')).lastTimetable)
    generated_timetable = Scheduler.compute(username)
    differences = get_differences(last_timetable, generated_timetable)
    generated_timetable_dump = json.dumps(generated_timetable)
    save_last_timetable(generated_timetable_dump, username)
    return JsonResponse(generated_timetable)


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


def health(request):
    return JsonResponse(data={'status': 'good'})


@api_view(['GET'])
def user_schedule(request, username):
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
    school_act_qs = UserSchoolActivity.objects.filter(user__email=f'{username}@gmail.com')
    for user_activity in school_act_qs:
        activity_dict = model_to_dict(user_activity.school_activity)
        frequency = activity_dict.pop('frequency')
        day = activity_dict.pop('day').lower()
        if frequency == 'full':
            to_return[1][day].append(activity_dict)
            to_return[2][day].append(activity_dict)
        elif frequency == 'par':
            to_return[2][day].append(activity_dict)
        else:
            to_return[1][day].append(activity_dict)

    return JsonResponse(data=to_return)
