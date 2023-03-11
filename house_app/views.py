from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from house_app.forms import HouseForm
from house_app.models import House, Apartment


# Create your views here.

class HousesList(ListView):
    model = House
    template_name = 'houses_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = House.objects.all()
        if self.request.GET.get('name'):
            object_list = object_list.filter(name__contains=self.request.GET.get('name'))
        if self.request.GET.get('address'):
            object_list = object_list.filter(address__contains=self.request.GET.get('address'))
        if self.request.GET.get('filter-name') == '1':
            object_list = object_list.order_by('-name')
        if self.request.GET.get('filter-name') == '0':
            object_list = object_list.order_by('name')
        if self.request.GET.get('filter-address') == '1':
            object_list = object_list.order_by('-address')
        if self.request.GET.get('filter-address') == '0':
            object_list = object_list.order_by('address')

        context['object_list'] = object_list
        return context
class HouseDetail(DetailView):
    model = House
    template_name = 'house_detail.html'

class HouseCreate(CreateView):
    model = House
    template_name = 'house_create.html'
    form_class = HouseForm
    success_url = reverse_lazy('houses_list')

class HouseUpdate(UpdateView):
    model = House
    template_name = 'house_update.html'
    form_class = HouseForm
    success_url = reverse_lazy('houses_list')

def house_delete(request, pk):
    item = get_object_or_404(House, id=pk)
    item.delete()
    return redirect('houses_list')


class ApartmentDetail(DetailView):
    model = Apartment
    template_name = 'apartment_detail.html'