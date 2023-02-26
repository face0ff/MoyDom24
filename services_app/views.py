from django.db import IntegrityError
from django.http import HttpResponseRedirect, request, JsonResponse, HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib import messages
from copy import deepcopy


from services_app.forms import ServicesForm, ServicesFormSet, UnitFormSet, TariffForm, PriceTariffServicesFormset, \
    PriceTariffServicesForm, RequisiteForm, ItemForm
from services_app.models import Services, Unit, Tariff, PriceTariffServices, Requisite, Item


class ServicesAdmin(CreateView):
    model = Services
    template_name = 'services.html'
    form_class = ServicesForm
    qs = Services.objects.all()
    success_url = reverse_lazy('services')



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services_formset'] = ServicesFormSet(queryset=self.qs, prefix='services')
        context['unit_formset'] = UnitFormSet(queryset=Unit.objects.all(), prefix='unit')
        context['use_unit_id'] = [x.unit.id for x in Services.objects.select_related('unit').all()]
        return context

    def post(self, *args, **kwargs):
        self.object = None
        services_formset = ServicesFormSet(self.request.POST, self.request.FILES, prefix='services')
        unit_formset = UnitFormSet(self.request.POST, self.request.FILES, prefix='unit')


        if all([unit_formset.is_valid(), services_formset.is_valid()]):
            return self.form_valid(unit_formset, services_formset)
        else:
            return self.form_invalid(unit_formset, services_formset)

    def form_valid(self, unit_formset, services_formset):
        print(self.request.POST)
        items = unit_formset.save(commit=False)
        for item in unit_formset.deleted_objects:
            item.delete()
        for item in items:
            item.save()
        items = services_formset.save(commit=False)
        for item in services_formset.deleted_objects:
            item.delete()
        for item in items:
            item.save()

        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, unit_formset, services_formset, **kwargs):
        print(unit_formset.errors)
        print(services_formset.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(unit_formset=unit_formset, services_formset=services_formset))


class TariffsList(ListView):
    model = Tariff
    template_name = 'tariffs_list.html'

class TariffDetail(DetailView):
    model = Tariff
    template_name = 'tariff.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        inst = get_object_or_404(Tariff, id=self.get_object().pk)
        context['all_in'] = PriceTariffServices.objects.select_related('services', 'services__unit').filter(tariff_id=inst.pk)
        return context


class TariffCreate(CreateView):
    model = Tariff
    template_name = 'tariff_create.html'
    form_class = TariffForm
    success_url = reverse_lazy('tariffs')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('pk') != None:
            inst = get_object_or_404(Tariff, id=self.kwargs.get('pk'))

            context['tariff'] = TariffForm(instance=inst)
            context['price_formset'] = PriceTariffServicesFormset(
                queryset=PriceTariffServices.objects.filter(tariff_id=self.get_object().pk),
                prefix='price')
        else:

            context['tariff'] = TariffForm()
            context['unit'] = Unit.objects.all()
            context['price_formset'] = PriceTariffServicesFormset(queryset=PriceTariffServices.objects.none(), prefix='price')
        return context

    def post(self, *args, **kwargs):
        print(self.request.POST)
        self.object = None
        qs_tariff = PriceTariffServices.objects.filter(tariff_id=self.request.GET.get('id'))
        tariff_form = TariffForm(self.request.POST)
        price_formset = PriceTariffServicesFormset(self.request.POST or None, queryset=PriceTariffServices.objects.none(),
                                                   prefix='price', initial=[{'services': tar.services, 'price': tar.price,
                                                    'unit': tar.services.unit} for tar in qs_tariff])

        if all([tariff_form.is_valid(), price_formset.is_valid()]):
            return self.form_valid(tariff_form, price_formset)
        else:
            return self.form_invalid(tariff_form, price_formset)

    def form_valid(self, tariff_form, price_formset):
        print(self.request.POST)
        tariff_form.save()
        price_formset.save(commit=False)

        for form in price_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.tariff = tariff_form.instance
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(tariff_form, price_formset)
        for form in price_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, tariff_form, price_formset, **kwargs):
        print(tariff_form.errors)
        print(price_formset.errors)

        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(tariff_form=tariff_form, price_formset=price_formset))



class TariffUpdate(UpdateView):
    model = Tariff
    template_name = 'tariff_update.html'
    form_class = TariffForm
    success_url = reverse_lazy('tariffs')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tariff'] = TariffForm(instance=get_object_or_404(Tariff, id=self.get_object().pk))
        context['price_formset'] = PriceTariffServicesFormset(queryset=PriceTariffServices.objects.filter(tariff_id=self.get_object().pk),
                                                              prefix='price')
        return context

    def post(self, *args, **kwargs):
        self.object = None
        tariff_form = TariffForm(self.request.POST, self.request.FILES, instance=get_object_or_404(Tariff, id=self.get_object().pk))
        price_formset = PriceTariffServicesFormset(self.request.POST or None,
                                                   queryset=PriceTariffServices.objects.filter(tariff_id=self.get_object().pk),
                                                   prefix='price')

        if all([tariff_form.is_valid(), price_formset.is_valid()]):
            return self.form_valid(tariff_form, price_formset)
        else:
            return self.form_invalid(tariff_form, price_formset)

    def form_valid(self, tariff_form, price_formset):
        print(self.request.POST)
        tariff_form.save()
        price_formset.save(commit=False)
        for form in price_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.tariff = tariff_form.instance
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(tariff_form, price_formset)
        for form in price_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, tariff_form, price_formset, **kwargs):
        print(tariff_form.errors)
        print(price_formset.errors)

        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(tariff_form=tariff_form, price_formset=price_formset))



class Requisite(CreateView):
    model = Requisite
    template_name = 'requisite.html'
    form_class = RequisiteForm
    success_url = reverse_lazy('requisite')
    inst = get_object_or_404(Requisite, id=1)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RequisiteForm(instance=self.inst)
        return context

    def post(self, *args, **kwargs):
        self.object = None
        form = RequisiteForm(self.request.POST or None, instance=self.inst)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        print(form.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(form=form))


class ItemList(ListView):
    model = Item
    template_name = 'items_list.html'
    def get_queryset(self):
        queryset = Item.objects.all()
        print(self.request.GET)
        if self.request.GET.get('filter') == '0':
            queryset = queryset.order_by('income_invoice')
        if self.request.GET.get('filter') == '1':
            queryset = queryset.order_by('-income_invoice')
        return queryset


class ItemCreate(CreateView):
    model = Item
    template_name = 'item_create.html'
    form_class = ItemForm
    success_url = reverse_lazy('items')


class ItemUpdate(UpdateView):
    model = Item
    template_name = 'item_update.html'
    form_class = ItemForm
    success_url = reverse_lazy('items')


def item_delete(request, pk):
    item = get_object_or_404(Item, id=pk)
    item.delete()
    return redirect('items')


def tariff_delete(request, pk):
    tariff = get_object_or_404(Tariff, id=pk)
    tariff.delete()
    return redirect('tariffs')

def show_unit_service(request):
    # if request.is_ajax():
    service_id = request.GET.get('service_id')

    unit_name = Services.objects.filter(id=service_id).values('unit__name')
    print(unit_name)
    response = {
        'services_price': list(unit_name)
    }
    return JsonResponse(response, status=200)

