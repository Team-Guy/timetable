from schedule.models import User, SchoolActivity, UserSchoolActivity
from .facultyactivity import FacultyActivity
from authentication.models import Preference
from .pref import Pref


def get_all_faculty_activities(username):
    username = username + "@gmail.com"
    user = User.objects.get(email=username)
    school_activities = UserSchoolActivity.objects.filter(user=user)
    return [FacultyActivity(activity) for activity in school_activities]


def get_faculty_activity_by_id(id):
    return FacultyActivity(SchoolActivity.objects.get(id=id))


def get_user_preferences(username):
    username = username + "gmail.com"
    user = User.objects.get(email=username)
    return Pref(Preference.objects.get(user=user))


def get_faculty_activities(*, prof=None, subject=None, type=None, spec=None):
    if not prof and not subject and not type and not spec:
        return [FacultyActivity(activity) for activity in SchoolActivity.objects.all()]


