"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class OrganizationInstanceForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset = Organization.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'organization-autocomplete')
    )

    conductors = forms.ModelChoiceField(
        queryset = Conductor.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'conductor-autocomplete')
    )

    class Meta:
        model = OrganizationInstance
        fields = ('__all__')