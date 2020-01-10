from django.urls import path, include
import authentication.views as auth_views

urlpatterns = [
    path('register/', auth_views.register),
    path('preferences/<str:username>', auth_views.preferences),
    path('optionals/<str:username>', auth_views.optionals),
    path('edit/<str:username>', auth_views.edit_profile),
    path('exists/<str:username>',auth_views.exists),
    path('optionals', auth_views.all_optionals),
    path('optionals/semester/<str:semester>', auth_views.optionals_by_semester),
    path('updateDB', auth_views.updateDB)
]
