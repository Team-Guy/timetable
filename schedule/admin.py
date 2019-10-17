from django.contrib import admin

# Register your models here.
from schedule.models import User, Activity

admin.site.register(User)
admin.site.register(Activity)
