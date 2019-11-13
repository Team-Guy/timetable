from schedule.models import User, UserExtraActivity
from .extraactivity import ExtraActivity


def get_extra_activities(username):
    username = username + "@gmail.com"
    user = User.objects.get(email=username)
    extra_activities = UserExtraActivity.objects.filter(user=user)
    return [ExtraActivity(activity) for activity in extra_activities]
