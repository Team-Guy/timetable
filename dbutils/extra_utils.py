from schedule.models import User, UserExtraActivity, ExtraActivity
from .extra_activity import ExtraFacActivity


def get_extra_activities(username):
    username = username + "@gmail.com"
    user = User.objects.get(email=username)
    extra_activities = UserExtraActivity.objects.filter(user=user)
    return [ExtraFacActivity(activity.extra_activity) for activity in extra_activities]


def get_extra_activity_by_id(id):
    return ExtraFacActivity(ExtraActivity.objects.get(id=id))
