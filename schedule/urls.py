from django.urls import path

from schedule import views

urlpatterns = [
    path('activities/', views.list_activities),
]
