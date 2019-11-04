from django.contrib import admin

# Register your models here.
from schedule.models import User, SchoolActivity

admin.site.register(User)
admin.site.register(SchoolActivity)
