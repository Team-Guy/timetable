from django.urls import path, include
import authentication.views as auth_views

urlpatterns = [
    path('register/', auth_views.register),
    path('preferences/<int:user_id>',auth_views.preferences)
]
