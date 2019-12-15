from django.contrib import admin

# Register your models here.
from authentication.models import LastTimetable, Preference

admin.site.register(LastTimetable)
admin.site.register(Preference)