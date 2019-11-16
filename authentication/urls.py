from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import authentication.views as auth_views

urlpatterns = [
    path('register/', auth_views.RegisterView.as_view()),
    path('preferences/<str:username>', auth_views.PreferencesView.as_view()),
    path('optionals/<str:username>', auth_views.OptionalsView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
