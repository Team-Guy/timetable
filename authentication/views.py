from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from authentication.models import Preference
from schedule.models import User
import json


# Create your views here.


def _process_register(post_body):
    post = json.loads(post_body)
    # print(post)
    # User.objects.all().delete()
    user = User(
        uid=post["uid"],
        name=post["name"],
        group=post["group"],
        email=post["email"],
        photo_url=post["photo"]
    )
    user.save()
    pref = Preference(
        user=user,
        preference1=False,
        preference2=False,
        preference3=False,
        preference1_prio='LOW',
        preference2_prio='LOW',
        preference3_prio='LOW'
    )
    pref.save()
    return user.uid


# @csrf_exempt
def register(request):
    uid = -1
    if request.method == "POST":
        uid = _process_register(request.body)
    return HttpResponse(str(uid))


def _process_preferences(post_body, user_id):
    post = json.loads(post_body)
    user = User.objects.get(id=user_id)
    # print(post["preference1"])
    preference = Preference(
        user=user,
        preference1=post["preference1"],
        preference2=post["preference2"],
        preference3=post["preference3"],
        preference1_prio=post["pref1_prio"],
        preference2_prio=post["pref2_prio"],
        preference3_prio=post["pref3_prio"]
    )
    # print(preference)
    preference.save()
    return user_id


# @csrf_exempt
def preferences(request, user_id):
    pid = -1
    if request.method == "POST":
        pid = _process_preferences(request.body, user_id)
    return HttpResponse(str(pid))
