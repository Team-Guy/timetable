from django.urls import path, include
import auth.views as auth_views

urlpatterns = [
    path('register/', auth_views.register)
]
