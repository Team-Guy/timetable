from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dbutils.optional import Optional
from authentication.models import Preference
from dbutils.school_utils import get_user_preferences, get_faculty_activities, remove_peda_sport
from schedule.models import User, UserSchoolActivity, SchoolActivity
from scrapping.main import getAll
import json

# Create your views here.

# def _add_school_activities_for_a_user(user: User):
#     group = user.group
#     school_act_qs = SchoolActivity.objects.filter(group=group)
#     for i in school_act_qs:
#         if i.title not in Optional.optional:
#             user_school_act = UserSchoolActivity(
#                 user=user,
#                 school_activity=i
#             )
#             user_school_act.save()
from scrapping.serie import Serie


def _process_register(post_body):
    post = json.loads(post_body)
    print(post)
    # User.objects.all().delete()
    user = User(
        uid=post["uid"],
        name=post["name"],
        group=post["group"],
        email=post["email"],
        photo_url=post["photo"]
    )
    user.save()
    # _add_school_activities_for_a_user(user)
    pref = Preference(
        user=user,
    )
    pref.save()
    return user.uid


@csrf_exempt
def register(request):
    uid = -1
    if request.method == "POST":
        uid = _process_register(request.body)
    ret = {"id": uid}
    return JsonResponse(ret)


def _process_preferences(post_body, username):
    post = json.loads(post_body)
    user = User.objects.get(email=username)
    # print(post["preference1"])
    preference = Preference(
        user=user,
        mondayStart=post['mondayStart'],
        tuesdayStart=post['tuesdayStart'],
        wednesdayStart=post['wednesdayStart'],
        thursdayStart=post['thursdayStart'],
        fridayStart=post['fridayStart'],
        mondayEnd=post['mondayEnd'],
        tuesdayEnd=post['tuesdayEnd'],
        wednesdayEnd=post['wednesdayEnd'],
        thursdayEnd=post['thursdayEnd'],
        fridayEnd=post['fridayEnd'],
        mondayMax=post['mondayMax'],
        tuesdayMax=post['tuesdayMax'],
        wednesdayMax=post['wednesdayMax'],
        thursdayMax=post['thursdayMax'],
        fridayMax=post['fridayMax']
    )
    # print(preference)
    preference.save()
    return user.id


@csrf_exempt
def preferences(request, username):
    pid = -1
    if request.method == "POST":
        username = username + "@gmail.com"
        pid = _process_preferences(request.body, username)
        ret = {"id": pid}
        return JsonResponse(ret)
    elif request.method == "GET":
        return JsonResponse(get_user_preferences(username).to_dict())
    else:
        return JsonResponse({"id": -1})


def _process_optionals(post_body, username):
    post = json.loads(post_body)
    user = User.objects.get(email=username)
    user.sport = post["sport"]
    user.peda = post["peda"]
    optionale = []
    for optional in post['optionals']:
        optionale.append(optional)
    school_activities = SchoolActivity.objects.filter(group=user.group)
    for activity in school_activities:
        if activity.title not in Optional.optional:
            if activity.title == Optional.sport and (not user.sport):
                continue
            if activity.title in Optional.peda and (not user.peda):
                continue
            user_activity = UserSchoolActivity(
                user=user,
                school_activity=activity
            )
            user_activity.save()
    for optional in optionale:
        s_activity = SchoolActivity.objects.filter(title=optional, group=user.group)
        for activity in s_activity:
            user_activity = UserSchoolActivity(
                user=user,
                school_activity=activity
            )
            user_activity.save()
    user.save()
    return 1


@csrf_exempt
def optionals(request, username):
    username = username + "@gmail.com"
    rid = -1
    if request.method == "POST":
        rid = _process_optionals(request.body, username)
    ret = {"id": rid}
    return JsonResponse(ret)


def optionals(request):
    return JsonResponse(Optional.optional, safe=False)


def _process_edit_post(post_body, username):
    user = User.objects.get(email=username)
    post = json.loads(post_body)
    user.group = post['group']
    user.save()
    UserSchoolActivity.objects.filter(user=user).delete()
    _process_optionals(post_body, username)
    return user.id


def _process_edit_get(username):
    user = User.objects.get(email=username)
    get = {}
    get['group'] = user.group
    get['sport'] = user.sport
    get['peda'] = user.peda
    get['optionals'] = []
    for u_activity in UserSchoolActivity.objects.filter(user=user):
        activity = u_activity.school_activity
        print(activity.title)
        if activity.title in Optional.optional and activity.title not in get['optionals']:
            get['optionals'].append(activity.title)

    return get


@csrf_exempt
def edit_profile(request, username):
    username = username + "@gmail.com"
    if request.method == "POST":
        uid = _process_edit_post(request.body, username)
        return JsonResponse({"id": uid})
    if request.method == "GET":
        return JsonResponse(_process_edit_get(username))


@csrf_exempt
def updateDB(request):
    getAll()
    return HttpResponse("DB updated")
