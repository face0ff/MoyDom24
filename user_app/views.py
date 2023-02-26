from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from user_app.forms import RoleFormSet, RoleForm
from user_app.models import Role


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