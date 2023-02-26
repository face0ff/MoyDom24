from django.urls import path

from user_app.views import Roles

urlpatterns = [
    path('roles/', Roles.as_view(), name='roles'),


]