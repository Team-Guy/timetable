from django.urls import path, include
import authentication.views as auth_views

urlpatterns = [
    path('register/', auth_views.register),
    path('preferences/<str:username>', auth_views.preferences),
    path('optionals/<str:username>', auth_views.optionals)
]
