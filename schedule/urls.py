from django.urls import path
import schedule.views
from django.urls import path

import schedule.views

urlpatterns = [
    path('', schedule.views.index),
]
