import json

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view

from authentication.models import LastTimetable
from dbutils.specialization import Specialization
from dbutils.timetable_utils import save_last_timetable, get_differences, get_last_timetable
from schedule.models import SchoolActivity, ExtraActivity, UserExtraActivity, User
from schedule.models import UserSchoolActivity
from schedule.serializers import SchoolActivitySerializer, ExtraActivitySerializer
from schedule.services import Scheduler
from datetime import datetime

from scrapping.serie import Serie


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
    last_timetable = get_last_timetable(username)
    generated_timetable = Scheduler.compute(username)
    response = JsonResponse(generated_timetable)
    differences = get_differences(last_timetable, generated_timetable)
    save_last_timetable(response.content.decode('utf-8'), username)
    return response


def get_activities(activity_type: str, username: str):
    odd_days_dict = dict(
        Monday={8: None,
                9: None,
                10: None,
                11: None,
                12: None,
                13: None,
                14: None,
                15: None,
                16: None,
                17: None,
                18: None,
                19: None
                },
        Tuesday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        },
        Wednesday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        },
        Thursday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        },
        Friday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        }
    )
    even_days_dict = dict(
        Monday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        },
        Tuesday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        },
        Wednesday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        },
        Thursday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        },
        Friday={
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None
        }
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
        day = activity_dict.get('day')
        start_hour = activity_dict.get('start_time').hour
        duration = activity_dict.get('duration')
        print(start_hour, duration)
        if frequency == 'full':
            for i in range(duration):
                to_return[1][day][start_hour+i]=activity_dict
                to_return[2][day][start_hour+i]=activity_dict
        elif frequency == 'even':
            for i in range(duration):
                to_return[2][day][start_hour+i]=activity_dict
        else:
            for i in range(duration):
                to_return[1][day][start_hour+i]=activity_dict
    return to_return


def health(request):
    return JsonResponse(data={'status': 'good'})


@api_view(['POST', 'GET'])
def save_last(request, username):
    if request.method == 'POST':
        save_last_timetable(json.dumps(request.data), username)
        return JsonResponse({"id": 1})
    elif request.method == 'GET':
        dict = get_last_timetable(username)
        return JsonResponse(dict)


@api_view(['POST'])
def save_extra(request, username):
    username = username + '@gmail.com'
    user = User.objects.get(email=username)
    lst = LastTimetable.objects.get(user=user)
    last = lst.lastTimetable
    lastDict = json.loads(last)
    lastDict['extra'] = request.data
    lst.lastTimetable = json.dumps(lastDict)
    lst.save()

    return JsonResponse({"id": 1})


@api_view(['GET'])
def get_groups(request):
    return JsonResponse(Specialization.groups[Serie.I1] +
                        Specialization.groups[Serie.I2] +
                        Specialization.groups[Serie.I3] +
                        Specialization.groups[Serie.IE1] +
                        Specialization.groups[Serie.IE2] +
                        Specialization.groups[Serie.IE3] +
                        Specialization.groups[Serie.MI1] +
                        Specialization.groups[Serie.MI2] +
                        Specialization.groups[Serie.MI3] +
                        Specialization.groups[Serie.MIE1] +
                        Specialization.groups[Serie.MIE1] +
                        Specialization.groups[Serie.MIE1], safe=False)
