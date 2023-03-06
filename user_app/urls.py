from django.urls import path

from user_app import views
from user_app.views import *

urlpatterns = [
    path('roles/', Roles.as_view(), name='roles'),
    path("admin/users_list/", UsersList.as_view(), name='users_list'),
    path("admin/user/<int:pk>", UserDetail.as_view(), name='user_detail'),
    path("admin/user/create/", UserCreate.as_view(), name='user_create'),
    path("admin/user/update/<int:pk>", UserUpdate.as_view(), name='user_update'),
    path("admin/user/delete/<int:pk>", views.user_delete, name='user_delete'),
    path('admin/user/', get_data, name='get_data'),

]