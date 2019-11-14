# Create your models here.
from django.db.models import Model, CharField, TimeField, IntegerField, TextField, EmailField, ForeignKey, CASCADE


class User(Model):
    uid = CharField(primary_key=True, max_length=255)
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    group = CharField(max_length=10)
    photo_url = CharField(max_length=255)


class Activity(Model):
    title = CharField(max_length=255)
    location = CharField(max_length=255)
    start_time = TimeField()
    day = CharField(max_length=15)
    duration = IntegerField(default=2)
    frequency = CharField(max_length=5)
    priority = CharField(max_length=30)


class ExtraActivity(Activity):
    description = TextField()


class SchoolActivity(Activity):
    type = CharField(max_length=30)
    professor = CharField(max_length=255)
    group = CharField(max_length=10)


class UserSchoolActivity(Model):
    school_activity = ForeignKey(to=SchoolActivity, on_delete=CASCADE)
    user = ForeignKey(to=User, on_delete=CASCADE)


class UserExtraActivity(Model):
    extra_activity = ForeignKey(to=ExtraActivity, on_delete=CASCADE)
    user = ForeignKey(to=User, on_delete=CASCADE)
