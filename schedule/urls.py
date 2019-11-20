from django.urls import path, include
from rest_framework.routers import DefaultRouter

from schedule import views

router = DefaultRouter()
router.register('school_act', views.SchoolActivityViewset, base_name='school_activity')
router.register('extra_act', views.ExtraActivityViewset, base_name='extra_activity')

urlpatterns = [
    path('', views.index),
    path('<str:username>', views.user_schedule),
    path('<str:username>/extra', views.user_extra_schedule),
    path('', include(router.urls)),
    path('algo', views.testalgo)
]
