from django.urls import path

from house_app import views
from house_app.views import *

urlpatterns = [

    path("admin/houses_list/", HousesList.as_view(), name='houses_list'),
    path("admin/house/<int:pk>", HouseDetail.as_view(), name='house_detail'),
    path("admin/house/create/", HouseCreate.as_view(), name='house_create'),
    path("admin/house/delete/<int:pk>", views.house_delete, name='house_delete'),
    path("admin/house/update/<int:pk>", HouseUpdate.as_view(), name='house_update'),
    path("select_user/", select_user, name='select_user'),

    path("admin/apartment_list/", ApartmentsList.as_view(), name='apartments_list'),
    path("admin/apartment/<int:pk>", ApartmentDetail.as_view(), name='apartment_detail'),
    path("admin/apartment/create/", ApartmentCreate.as_view(), name='apartment_create'),
    path("admin/apartment/delete/<int:pk>", views.apartment_delete, name='apartment_delete'),
    path("admin/apartment/update/<int:pk>", ApartmentUpdate.as_view(), name='apartment_update'),
    path("select_house/", select_house, name='select_house'),

    path("admin/requests_list/", RequestsList.as_view(), name='requests_list'),
    path("admin/request/<int:pk>", RequestDetail.as_view(), name='request_detail'),
    path("admin/request/create/", RequestCreate.as_view(), name='request_create'),
    path("admin/request/update/<int:pk>", RequestUpdate.as_view(), name='request_update'),
    path("admin/request/delete/<int:pk>", views.request_delete, name='request_delete'),




]