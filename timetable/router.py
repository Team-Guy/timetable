from schedule.api.viewsets import ActivitesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('activities', ActivitesViewSet, base_name='activities')