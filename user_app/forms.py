from django.forms import ModelForm, modelformset_factory

from user_app.models import Role


class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ('role',)


RoleFormSet = modelformset_factory(Role, form=RoleForm, extra=0)