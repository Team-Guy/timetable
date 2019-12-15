from django.urls import path, include
from rest_framework.routers import DefaultRouter

from schedule import views

router = DefaultRouter()
router.register('school_act', views.SchoolActivityViewset, base_name='school_activity')
router.register('extra_act', views.ExtraActivityViewset, base_name='extra_activity')

urlpatterns = [
    path('<str:username>', views.user_schedule),
    path('extra/<str:username>', views.user_extra_schedule),
    path('initial/<str:username>', views.get_initial_timetable),
    path('save_last/<str:username>', views.save_last),
    path('save_extra/<str:username>', views.save_extra),
    path('groups/', views.get_groups),
    path('', include(router.urls)),
    path('algo/<str:username>/', views.testalgo)
]
