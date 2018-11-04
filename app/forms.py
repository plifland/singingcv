"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance, Genre, Composition

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

### Contacts page
class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

### Data input
class OrganizationInstanceForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset = Organization.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'organization-autocomplete', attrs={'data-html': True})
    )

    conductors = forms.ModelMultipleChoiceField(
        queryset = Conductor.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'conductor-autocomplete')
    )

    associateconductors = forms.ModelMultipleChoiceField(
        queryset = Conductor.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'conductor-autocomplete')
    )

    administrators = forms.ModelMultipleChoiceField(
        queryset = Conductor.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'administrator-autocomplete', attrs={'data-html': True})
    )

    singerspaid = forms.ModelMultipleChoiceField(
        queryset = Singer.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'singer-autocomplete', attrs={'data-html': True})
    )

    singersvolunteer = forms.ModelMultipleChoiceField(
        queryset = Singer.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'singer-autocomplete', attrs={'data-html': True})
    )

    class Meta:
        model = OrganizationInstance
        fields = ('__all__')

class CompositionForm(forms.ModelForm):
    composer = forms.ModelChoiceField(
        queryset = Composer.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'composer-autocomplete', attrs={'data-html': True}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset = Genre.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'genre-autocomplete', attrs={'data-html': True}),
    )

    class Meta:
        model = Composition
        fields = ('__all__')

class ComposerForm(forms.ModelForm):
    person = forms.ModelChoiceField(
        queryset = Person.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'person-autocomplete', attrs={'data-html': True, 'data-minimum-input-length': 2, })
    )

    class Meta:
        model = Composer
        fields = ('__all__')

class GenreForm(forms.ModelForm):
    #def clean_subtype(self):
    #    data = self.cleaned_data['subtype']
    #    return data

    #def clean_name(self):
    #    data = self.cleaned_data['name']
    #    return data

    class Meta:
        model = Genre
        fields = ('__all__')