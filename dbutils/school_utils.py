from dbutils.optional import Optional
from dbutils.usr import Usr
from schedule.models import User, SchoolActivity, UserSchoolActivity
from .faculty_activity import FacultyActivity
from authentication.models import Preference
from .pref import Pref
from .specialization import Specialization


def get_current_user(username):
    username = username + "@gmail.com"
    user = User.objects.get(email=username)
    return Usr(user)


def get_all_faculty_activities(username):
    username = username + "@gmail.com"
    user = User.objects.get(email=username)
    school_activities = UserSchoolActivity.objects.filter(user=user)
    return [FacultyActivity(activity.school_activity) for activity in school_activities]


def get_faculty_activity_by_id(id):
    return FacultyActivity(SchoolActivity.objects.get(id=id))


def get_user_preferences(username):
    username = username + "@gmail.com"
    # print(username)
    user = User.objects.get(email=username)
    return Pref(Preference.objects.get(user=user))


def remove_peda_sport(list_classes, user):
    classes = []

    for cls in list_classes:
        if (not user.sport) and cls.title == Optional.sport:
            continue
        if (not user.peda) and cls.title in Optional.peda:
            continue
        classes.append(cls)

    return classes


def get_user_optionals(username):
    activities = get_all_faculty_activities(username)
    optionals = []
    titles = []
    for activity in activities:
        if activity.title in Optional.optional and activity.title not in titles:
            optionals.append(activity)
            titles.append(activity.title)
    return optionals


def get_faculty_activities(*, prof=None, subject=None, type=None, spec=None):
    if not prof and not subject and not type and not spec:  # 0
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.all()]
    elif not subject and not type and not spec:  # 1
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(professor=prof)]
    elif not prof and not type and not spec:  # 2
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(title=subject)]
    elif not prof and not subject and not spec:  # 3
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(type=type)]
    elif not prof and not subject and not type:  # 4
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend([FacultyActivity(activity) for activity in SchoolActivity.objects.filter(group=group)])
        return activities
    elif not type and not spec:  # 1 2
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(professor=prof, title=subject)]
    elif not subject and not spec:  # 1 3
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(professor=prof, type=type)]
    elif not subject and not type:  # 1 4
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend(
                [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(professor=prof, group=group)])
        return activities
    elif not prof and not spec:  # 2 3
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(title=subject, type=type)]
    elif not prof and not type:  # 2 4
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend(
                [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(title=subject, group=group)])
        return activities
    elif not prof and not subject:  # 3 4
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend(
                [FacultyActivity(activity) for activity in SchoolActivity.objects.filter(type=type, group=group)])
        return activities
    elif not spec:  # 1 2 3
        return [FacultyActivity(activity) for activity in
                SchoolActivity.objects.filter(professor=prof, title=subject, type=type)]
    elif not type:  # 1 2 4
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend(
                [FacultyActivity(activity) for activity in
                 SchoolActivity.objects.filter(professor=prof, title=subject, group=group)])
        return activities
    elif not subject:  # 1 3 4
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend(
                [FacultyActivity(activity) for activity in
                 SchoolActivity.objects.filter(professor=prof, type=type, group=group)])
        return activities
    elif not prof:  # 2 3 4
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend(
                [FacultyActivity(activity) for activity in
                 SchoolActivity.objects.filter(title=subject, type=type, group=group)])
        return activities
    else:
        activities = []
        for group in Specialization.groups[spec]:
            activities.extend(
                [FacultyActivity(activity) for activity in
                 SchoolActivity.objects.filter(professor=prof, subject=subject, type=type, group=group)])
        return activities
