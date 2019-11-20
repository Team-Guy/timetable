# Create your models here.
from django.db.models import Model, CharField, TimeField, IntegerField, TextField, EmailField, ForeignKey, CASCADE


class User(Model):
    uid = CharField(unique=True, max_length=255)
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    group = CharField(max_length=10)
    photo_url = CharField(max_length=255)


class SchoolActivity(Model):
    title = CharField(max_length=255)
    location = CharField(max_length=255)
    start_time = TimeField()
    day = CharField(max_length=15)
    group = CharField(max_length=10)
    professor = CharField(max_length=255)
    type = CharField(max_length=30)
    duration = IntegerField(default=2)
    frequency = CharField(max_length=5)
    priority = CharField(max_length=30)


class ExtraActivity(Model):
    title = CharField(max_length=255)
    location = CharField(max_length=255)
    start_time = TimeField()
    day = CharField(max_length=15)
    duration = IntegerField(default=2)
    frequency = CharField(max_length=5)
    priority = CharField(max_length=30)
    description = TextField()


class UserSchoolActivity(Model):
    school_activity = ForeignKey(to=SchoolActivity, on_delete=CASCADE)
    user = ForeignKey(to=User, on_delete=CASCADE)


class UserExtraActivity(Model):
    extra_activity = ForeignKey(to=ExtraActivity, on_delete=CASCADE)
    user = ForeignKey(to=User, on_delete=CASCADE)
