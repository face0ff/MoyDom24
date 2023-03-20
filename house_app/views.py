from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from house_app.forms import *
from house_app.models import House, Apartment, Section, Floor, Request
from user_app.models import UserProfile, Role


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


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_formset'] = SectionFormSet(queryset=Section.objects.none(), prefix='section')
        context['floor_formset'] = FloorFormSet(queryset=Floor.objects.none(), prefix='floor')
        context['user_formset'] = UserFormSet(prefix='user')
        context['house_form'] = HouseForm()
        return context

    def post(self, *args, **kwargs):
        print(self.request.POST)
        self.object = None
        house_form = HouseForm(self.request.POST, self.request.FILES)
        section_formset = SectionFormSet(self.request.POST, prefix='section')
        floor_formset = FloorFormSet(self.request.POST, prefix='floor')
        user_formset = UserFormSet(self.request.POST, prefix='user')


        if all([section_formset.is_valid(), floor_formset.is_valid(), user_formset.is_valid(), house_form.is_valid()]):
            return self.form_valid(section_formset, floor_formset, user_formset, house_form)
        else:
            return self.form_invalid(section_formset, floor_formset, user_formset, house_form)

    def form_valid(self, section_formset, floor_formset, user_formset, house_form):

        house = house_form.save(commit=False)
        house.save()
        section_formset.save(commit=False)
        floor_formset.save(commit=False)


        for form in section_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.house_id = house.id
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(section_formset, floor_formset, user_formset, house_form)
        for form in section_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")

        for form in floor_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.house_id = house.id
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(section_formset, floor_formset, user_formset, house_form)
        for form in floor_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")

        for form_user in user_formset:
            if form_user.cleaned_data and form_user.cleaned_data['DELETE'] is False:
                user = form_user.cleaned_data.get('user')
                house.users.add(user)

        # for form in user_formset.deleted_objects:
        #     form.delete()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, section_formset, floor_formset, user_formset, house_form, **kwargs):
        print(section_formset.errors)
        print(floor_formset.errors)
        print(user_formset.errors)
        print(house_form.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(section_formset=section_formset, floor_formset=floor_formset,
                                  user_formset=user_formset, house_form=house_form))

def select_user(request):
    if request.GET.get('user_id'):
        print(request.GET.get('user_id'))
        user_role = UserProfile.objects.get(pk=request.GET.get('user_id')).role.get_roles_display()
        role_id = UserProfile.objects.get(pk=request.GET.get('user_id')).role_id
        print(user_role)
        data = {
            'user_role': user_role,
            'role_id': role_id
        }
        return JsonResponse(data, status=200)


class HouseUpdate(UpdateView):
    model = House
    template_name = 'house_update.html'
    form_class = HouseForm
    success_url = reverse_lazy('houses_list')
    # queryset = House.objects.prefetch_related('users__role')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_formset'] = SectionFormSet(queryset=Section.objects.filter(house_id=self.get_object().pk), prefix='section')
        context['floor_formset'] = FloorFormSet(queryset=Floor.objects.filter(house_id=self.get_object().pk), prefix='floor')
        users = self.object.users.all()
        context['user_formset'] = UserFormSet(prefix='user', initial=[{'user': item.id,
                                                        'role': item.role.get_roles_display()} for item in users])
        context['house_form'] = HouseForm(instance=get_object_or_404(House, id=self.get_object().pk))
        return context

    def post(self, *args, **kwargs):
        print(self.request.POST)
        self.object = self.get_object()
        house_form = HouseForm(self.request.POST, self.request.FILES,
                               instance=get_object_or_404(House, id=self.get_object().pk))
        section_formset = SectionFormSet(self.request.POST, prefix='section',
                                         queryset=Section.objects.filter(house_id=self.get_object().pk))
        floor_formset = FloorFormSet(self.request.POST, prefix='floor',
                                     queryset=Floor.objects.filter(house_id=self.get_object().pk))
        user_formset = UserFormSet(self.request.POST, prefix='user' )


        if all([section_formset.is_valid(), floor_formset.is_valid(), user_formset.is_valid(), house_form.is_valid()]):
            return self.form_valid(section_formset, floor_formset, user_formset, house_form)
        else:
            return self.form_invalid(section_formset, floor_formset, user_formset, house_form)

    def form_valid(self, section_formset, floor_formset, user_formset, house_form):

        house = house_form.save(commit=False)
        house.save()
        section_formset.save(commit=False)
        floor_formset.save(commit=False)


        for form in section_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.house_id = house.id
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(section_formset, floor_formset, user_formset, house_form)
        for form in section_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")

        for form in floor_formset:
            if form.is_valid():
                item = form.save(commit=False)
                item.house_id = house.id
                try:
                    item.save()
                except IntegrityError:
                    pass
            else:
                return self.form_invalid(section_formset, floor_formset, user_formset, house_form)
        for form in floor_formset.deleted_objects:
            form.delete()
        messages.success(self.request, "Valid form")
        house.users.clear()
        for form_user in user_formset:
            if form_user.cleaned_data and form_user.cleaned_data['DELETE'] is False:
                user = form_user.cleaned_data.get('user')
                house.users.add(user)

        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, section_formset, floor_formset, user_formset, house_form, **kwargs):
        print(section_formset.errors)
        print(floor_formset.errors)
        print(user_formset.errors)
        print(house_form.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(section_formset=section_formset, floor_formset=floor_formset,
                                  user_formset=user_formset, house_form=house_form))

def house_delete(request, pk):
    item = get_object_or_404(House, id=pk)
    item.delete()
    return redirect('houses_list')


class ApartmentDetail(DetailView):
    model = Apartment
    template_name = 'apartment_detail.html'


class ApartmentsList(ListView):
    model = Apartment
    template_name = 'apartments_list.html'
    context_object_name = 'apartments'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        houses = House.objects.all()
        queryset = Apartment.objects.all()

        # personal_accounts = PersonalAccount.objects.select_related('apartment').all()
        # context['personal_accounts'] = personal_accounts
        # context['idx'] = [x.apartment.id for x in personal_accounts if x.apartment]

        if self.request.GET.get('filter-number') == '1':
            queryset = queryset.order_by('-number')
        if self.request.GET.get('filter-number') == '0':
            queryset = queryset.order_by('number')
        if self.request.GET.get('filter-house') == '1':
            queryset = queryset.order_by('-id')
        if self.request.GET.get('filter-house') == '0':
            queryset = queryset.order_by('id')
        if self.request.GET.get('filter-section') == '1':
            queryset = queryset.order_by('-section')
        if self.request.GET.get('filter-section') == '0':
            queryset = queryset.order_by('section')
        if self.request.GET.get('filter-floor') == '1':
            queryset = queryset.order_by('-floor')
        if self.request.GET.get('filter-floor') == '0':
            queryset = queryset.order_by('floor')
        if self.request.GET.get('filter-owner') == '0':
            queryset = queryset.order_by('-owner__last_name')
        if self.request.GET.get('filter-owner') == '1':
            queryset = queryset.order_by('owner__last_name')
        if self.request.GET.get('input_number'):
            queryset = queryset.filter(number__icontains=self.request.GET.get('input_number'))
        if self.request.GET.get('input_house'):
            queryset = queryset.filter(house_id=self.request.GET.get('input_house'))
        if self.request.GET.get('input_section'):
            queryset = queryset.filter(section__name=self.request.GET.get('input_section'))
        if self.request.GET.get('input_floor'):
            queryset = queryset.filter(floor__name=self.request.GET.get('input_floor'))
        if self.request.GET.get('input_owner'):
            queryset = queryset.filter(owner=self.request.GET.get('input_owner'))
        # if self.request.GET.get('debt'):
        #     if self.request.GET.get('debt') == 'yes':
        #         p_a = PersonalAccount.objects.select_related('apartment').filter(balance__lt=0)
        #         idx = [x.apartment.id for x in p_a if x.apartment]
        #     else:
        #         p_a = PersonalAccount.objects.select_related('apartment').filter(balance__gte=0)
        #         idx = [x.apartment.id for x in p_a if x.apartment]
        #     queryset = queryset.filter(pk__in=idx)
        if self.request.GET.get('input_house'):
            for house in houses:
                if house.id == int(self.request.GET.get('input_house')):
                    context['sections'] = Section.objects.filter(house=house.id)
                    context['floors'] = Floor.objects.filter(house=house.id)

        paginator = Paginator(queryset, 10)  # 3 posts in each page
        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            queryset = paginator.page(paginator.num_pages)

        context['page'] = page
        context['houses'] = houses
        context['owners'] = UserProfile.objects.filter(is_staff=False)
        context['apartments'] = queryset
        return context


class ApartmentCreate(CreateView):
    model = Apartment
    template_name = 'apartment_create.html'
    form_class = ApartmentForm
    success_url = reverse_lazy('apartments_list')


class ApartmentUpdate(UpdateView):
    model = Apartment
    template_name = 'apartment_update.html'
    form_class = ApartmentForm
    success_url = reverse_lazy('apartments_list')

    def form_valid(self, form):
        if 'action_save_add' in self.request.POST:
            # Получить последний идентификатор
            last_id = Apartment.objects.all().order_by('-id').first().id
            last_number = Apartment.objects.all().order_by('-id').first().number
            # Увеличить на единицу
            new_id = last_id + 1
            # Установить имя
            new_number = last_number + 1
            # Сохранить новые значения
            form.instance.id = new_id
            form.instance.number = new_number
            super(ApartmentUpdate, self).form_valid(form)
            return redirect('apartment_update', new_id)
        else:
            return super(ApartmentUpdate, self).form_valid(form)







def apartment_delete(request, pk):
    apart = get_object_or_404(Apartment, id=pk)
    apart.delete()
    return redirect('apartments_list')

def select_house(request):
    if request.GET.get('house_field'):
        house = House.objects.get(pk=request.GET.get('house_field'))
        section_house = house.section_set.all().values('id', 'name')
        floor_house = house.floor_set.all().values('id', 'name')
        print(section_house)
        print(floor_house)
        response = {
            'section_data': list(section_house),
            'floor_data': list(floor_house)
        }
        return JsonResponse(response, status=200)


class RequestDetail(DetailView):
    model = Request
    template_name = 'request_detail.html'


class RequestsList(ListView):
    model = Request
    template_name = 'requests_list.html'


class RequestCreate(CreateView):
    model = Request
    template_name = 'request_create.html'
    form_class = RequestForm
    success_url = reverse_lazy('requests_list')


class RequestUpdate(UpdateView):
    model = Request
    template_name = 'request_update.html'
    form_class = RequestForm
    success_url = reverse_lazy('requests_list')


def request_delete(request, pk):
    request = get_object_or_404(Request, id=pk)
    request.delete()
    return redirect('requests_list')
