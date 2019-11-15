from django.db.models import Model, OneToOneField, BooleanField, CASCADE, CharField
from schedule.models import User


# Create your models here.

class Preference(Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
    preference1 = BooleanField(default=False)
    preference2 = BooleanField(default=False)
    preference3 = BooleanField(default=False)
    preference1_prio = CharField(max_length=32)
    preference2_prio = CharField(max_length=32)
    preference3_prio = CharField(max_length=32)
