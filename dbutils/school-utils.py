from schedule.models import User, SchoolActivity, UserSchoolActivity
from .facultyactivity import FacultyActivity


def get_faculty_activities(username):
    username = username + "@gmail.com"
    user = User.objects.get(email=username)
    school_activities = UserSchoolActivity.objects.filter(user=user)
    return [FacultyActivity(activity) for activity in school_activities]
