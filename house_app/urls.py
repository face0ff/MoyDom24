from django.urls import path

from house_app import views
from house_app.views import *

urlpatterns = [

    path("admin/houses_list/", HousesList.as_view(), name='houses_list'),
    path("admin/house/<int:pk>", HouseDetail.as_view(), name='house_detail'),
    path("admin/house/create/", HouseCreate.as_view(), name='house_create'),
    path("admin/house/delete/<int:pk>", views.house_delete, name='house_delete'),
    path("admin/house/update/<int:pk>", HouseUpdate.as_view(), name='house_update'),


    path("admin/apartment/<int:pk>", ApartmentDetail.as_view(), name='apartment_detail'),




]