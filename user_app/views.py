from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib import messages
from user_app.forms import RoleFormSet, RoleForm, UserForm, UserUpdateForm
from user_app.models import Role, UserProfile


# Create your views here.

class Roles(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'roles.html'
    success_url = reverse_lazy('roles')
    qs = Role.objects.all()
    print(qs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_formset'] = RoleFormSet(queryset=self.qs, prefix='role')
        return context

    def post(self, *args, **kwargs):
        self.object = None
        formset = RoleFormSet(self.request.POST or None, queryset=self.qs, prefix='role')
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset):
        formset.save(commit=False)
        for form in formset:
            item = form.save(commit=False)
            item.save()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, formset, **kwargs):
        print(formset.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(formset=formset))


class UsersList(ListView):
    model = UserProfile
    template_name = 'users_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = UserProfile.objects.all()
        if self.request.GET.get('user'):
            object_list = object_list.filter(Q(last_name__icontains=self.request.GET.get('user')) |
                                       Q(first_name__icontains=self.request.GET.get('user')))
        if self.request.GET.get('role'):
            object_list = object_list.filter(role__roles=self.request.GET.get('role'))
        if self.request.GET.get('telephone'):
            object_list = object_list.filter(telephone__icontains=self.request.GET.get('telephone'))
        if self.request.GET.get('email'):
            object_list = object_list.filter(email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('status'):
            object_list = object_list.filter(status=self.request.GET.get('status'))
        paginator = Paginator(object_list, 3)  # 3 posts in each page
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            object_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            object_list = paginator.page(paginator.num_pages)

        # print(object_list.object_list)
        context['object_list'] = object_list
        context['page'] = page
        return context



class UserCreate(CreateView):
    model = UserProfile
    template_name = 'user_create.html'
    form_class = UserForm
    success_url = reverse_lazy('users_list')


class UserDetail(DetailView):
    model = UserProfile
    template_name = 'user_detail.html'


class UserUpdate(UpdateView):
    model = UserProfile
    template_name = 'user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_list')

def user_delete(request, pk):
    user = get_object_or_404(UserProfile, id=pk)
    user.delete()
    return redirect('users_list')


class OwnerDetail(DetailView):
    model = UserProfile
    template_name = 'owner_detail.html'