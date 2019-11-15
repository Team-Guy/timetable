from django.contrib import admin

# Register your models here.
from schedule.models import User, SchoolActivity, ExtraActivity, UserExtraActivity, UserSchoolActivity


admin.site.register(User)
admin.site.register(SchoolActivity)
admin.site.register(ExtraActivity)
admin.site.register(UserSchoolActivity)
admin.site.register(UserExtraActivity)
