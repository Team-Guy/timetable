from django.urls import path, include
from rest_framework.routers import DefaultRouter

from schedule import views

router = DefaultRouter()
router.register('school_act', views.SchoolActivityViewset, base_name='school_activity')
router.register('extra_act', views.ExtraActivityViewset, base_name='extra_activity')

urlpatterns = [
    path('', views.HelloView.as_view()),
    path('<str:username>', views.UserSchedule.as_view()),
    path('<str:username>/extra', views.UserExtraSchedule.as_view()),
    path('', include(router.urls))
]
