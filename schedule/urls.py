from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import schedule.views

router = routers.DefaultRouter()
router.register(r'schoolactivity', schedule.views.SchoolActivityViewset)
router.register(r'extraactivity', schedule.views.ExtraActivityViewset)

urlpatterns = [
    path('', schedule.views.index),
    path('<str:username>', schedule.views.user_schedule),
    path('/crud/', include(router.urls)),
]
