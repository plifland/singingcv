"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import site as admin_site
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from dal import autocomplete

from .models import *

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

class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs) 

### Replist filter
class RepListFiltersForm(forms.Form):
    composer = forms.ModelChoiceField(
        required=False,
        queryset = Composer.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'composer-autocomplete', attrs={'data-html': True}),
    )

    org = forms.ModelChoiceField(
        required=False,
        queryset = Organization.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'organization-autocomplete', attrs={'data-html': True}),
    )

    year = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={'size':10}),
    )

    formg = forms.ModelChoiceField(
        required=False,
        queryset = Genre.objects.filter(subtype='F'),
    )

    era = forms.ModelChoiceField(
        required=False,
        queryset = Genre.objects.filter(subtype='E'),
    )

    voicing = EmptyChoiceField(
        choices = Composition.VOICING_CHOICES,
        label="",
        initial='',
        empty_label="All",
        widget=forms.Select(),
        required=False,
    )

### Data input
class OrganizationInstanceForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset = Organization.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'organization-autocomplete', attrs={'data-html': True})
    )

    conductors = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Conductor.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'conductor-autocomplete')
    )

    associateconductors = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Conductor.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'conductor-autocomplete')
    )

    administrators = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Administrator.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'administrator-autocomplete', attrs={'data-html': True})
    )

    singerspaid = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Singer.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'singer-autocomplete', attrs={'data-html': True})
    )

    singersvolunteer = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Singer.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'singer-autocomplete', attrs={'data-html': True})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].widget = RelatedFieldWidgetWrapper( 
               self.fields['organization'].widget, 
               self.instance._meta.get_field('organization').remote_field,            
               admin_site,
           )
        self.fields['conductors'].widget = RelatedFieldWidgetWrapper( 
               self.fields['conductors'].widget, 
               self.instance._meta.get_field('conductors').remote_field,            
               admin_site,
           )
        self.fields['associateconductors'].widget = RelatedFieldWidgetWrapper( 
               self.fields['associateconductors'].widget, 
               self.instance._meta.get_field('associateconductors').remote_field,            
               admin_site,
           )
        self.fields['administrators'].widget = RelatedFieldWidgetWrapper( 
               self.fields['administrators'].widget, 
               self.instance._meta.get_field('administrators').remote_field,            
               admin_site,
           )
        self.fields['singerspaid'].widget = RelatedFieldWidgetWrapper( 
               self.fields['singerspaid'].widget, 
               self.instance._meta.get_field('singerspaid').remote_field,            
               admin_site,
           )
        self.fields['singersvolunteer'].widget = RelatedFieldWidgetWrapper( 
               self.fields['singersvolunteer'].widget, 
               self.instance._meta.get_field('singersvolunteer').remote_field,            
               admin_site,
           )

    class Meta:
        model = OrganizationInstance
        fields = ('__all__')

class CompositionForm(forms.ModelForm):
    composer = forms.ModelChoiceField(
        required=False,
        queryset = Composer.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'composer-autocomplete', attrs={'data-html': True}),
    )

    arranger = forms.ModelChoiceField(
        required=False,
        queryset = Composer.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'composer-autocomplete', attrs={'data-html': True}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset = Genre.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'genre-autocomplete', attrs={'data-html': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['composer'].widget = RelatedFieldWidgetWrapper( 
               self.fields['composer'].widget, 
               self.instance._meta.get_field('composer').remote_field,            
               admin_site,
           )
        self.fields['tags'].widget = RelatedFieldWidgetWrapper( 
               self.fields['tags'].widget, 
               self.instance._meta.get_field('tags').remote_field,            
               admin_site,
           )

    class Meta:
        model = Composition
        fields = ('__all__')    

class AdministratorForm(forms.ModelForm):
    person = forms.ModelChoiceField(
        queryset = Person.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'person-autocomplete', attrs={'data-html': True, 'data-minimum-input-length': 2, })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person'].widget = RelatedFieldWidgetWrapper( 
               self.fields['person'].widget, 
               self.instance._meta.get_field('person').remote_field,            
               admin_site,
           )

    class Meta:
        model = Administrator
        fields = ('__all__')
class ComposerForm(forms.ModelForm):
    person = forms.ModelChoiceField(
        queryset = Person.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'person-autocomplete', attrs={'data-html': True, 'data-minimum-input-length': 2, })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person'].widget = RelatedFieldWidgetWrapper( 
               self.fields['person'].widget, 
               self.instance._meta.get_field('person').remote_field,            
               admin_site,
           )

    class Meta:
        model = Composer
        fields = ('__all__')
class ConductorForm(forms.ModelForm):
    person = forms.ModelChoiceField(
        queryset = Person.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'person-autocomplete', attrs={'data-html': True, 'data-minimum-input-length': 2, })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person'].widget = RelatedFieldWidgetWrapper( 
               self.fields['person'].widget, 
               self.instance._meta.get_field('person').remote_field,            
               admin_site,
           )

    class Meta:
        model = Conductor
        fields = ('__all__')
class SingerForm(forms.ModelForm):
    person = forms.ModelChoiceField(
        queryset = Person.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'person-autocomplete', attrs={'data-html': True, 'data-minimum-input-length': 2, })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person'].widget = RelatedFieldWidgetWrapper( 
               self.fields['person'].widget, 
               self.instance._meta.get_field('person').remote_field,            
               admin_site,
           )

    class Meta:
        model = Singer
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

class PerformanceInstanceForm(forms.ModelForm):
    performance = forms.ModelChoiceField(
        queryset = Performance.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'performance-autocomplete', attrs={'data-html': True}),
    )

    organizations = forms.ModelMultipleChoiceField(
        queryset = OrganizationInstance.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'organizationinstance-autocomplete',
                                                   forward=['performanceinstance'],
                                                   attrs={'data-html': True},),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['performance'].widget = RelatedFieldWidgetWrapper( 
               self.fields['performance'].widget, 
               self.instance._meta.get_field('performance').remote_field,            
               admin_site,
           )
        self.fields['organizations'].widget = RelatedFieldWidgetWrapper( 
               self.fields['organizations'].widget, 
               self.instance._meta.get_field('organizations').remote_field,            
               admin_site,
           )

    class Meta:
        model = PerformanceInstance
        fields = ('__all__')

class PerformancePieceForm(forms.ModelForm):
    performanceinstance = forms.ModelChoiceField(
        queryset = PerformanceInstance.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'performanceinstance-autocomplete', attrs={'data-html': True}),
    )

    organizations = forms.ModelMultipleChoiceField(
        queryset = OrganizationInstance.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url = 'organizationinstance-autocomplete',
                                                   forward=['performanceinstance'],
                                                   attrs={'data-html': True},),
    )

    composition = forms.ModelChoiceField(
        queryset = Composition.objects.all(),
        widget = autocomplete.ModelSelect2(url = 'composition-autocomplete', attrs={'data-html': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['performanceinstance'].widget = RelatedFieldWidgetWrapper( 
               self.fields['performanceinstance'].widget, 
               self.instance._meta.get_field('performanceinstance').remote_field,            
               admin_site,
           )
        self.fields['organizations'].widget = RelatedFieldWidgetWrapper( 
               self.fields['organizations'].widget, 
               self.instance._meta.get_field('organizations').remote_field,            
               admin_site,
           )
        self.fields['composition'].widget = RelatedFieldWidgetWrapper( 
               self.fields['composition'].widget, 
               self.instance._meta.get_field('composition').remote_field,            
               admin_site,
           )

    class Meta:
        model = Composition
        fields = ('__all__')