# Create your views here.

from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework.decorators import api_view

from schedule.models import UserSchoolActivity


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
        elif frequency == 'even':
            to_return[2][day].append(activity_dict)
        else:
            to_return[1][day].append(activity_dict)

    return JsonResponse(data=to_return)


def index(request):
    # getInfo(Link.IE2)
    return HttpResponse("yay")
