import datetime

from django.db.models import Max,Q
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.views import generic
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect
from django.template.loader import get_template
from django.contrib import messages

from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance, Performance, PerformanceInstance, PerformancePiece, Composition
from .forms import ContactForm, OrganizationInstanceForm

def vocalcv(request):
    # Gets the most recent record per organization
    organizations = Organization.objects.values('id').annotate(maxyear=Max('organizationinstance__year'))
    organizationinstances = OrganizationInstance.objects.filter(Q(organization__in=[o['id'] for o in organizations]) & Q(year__in=[o['maxyear'] for o in organizations]))

    # Let's add a filter for upcoming performances
    performances = PerformanceInstance.objects.all().filter(date__gte = datetime.date.today())
    #performance_orgs = []
    #for prf in performances:
    #    for org in prf.organizations.all():
    #        performance_orgs.append(org.organization.id)
    #performance_orgs = list(set(performance_orgs))
    performance_orgs = list(set(performances.values_list('organizations__organization', flat=True)))
    activeorgs = organizationinstances.filter(Q(organization__in=performance_orgs))
    inactiveorgs = organizationinstances.exclude(Q(organization__in=performance_orgs))

    org_count = Organization.objects.count()
    conductor_count = Conductor.objects.count()
    piece_count = Composition.objects.count()
    
    return render(
        request,
        'vocalcv.html',
        context={'activeorgs':activeorgs
                 ,'inactiveorgs':inactiveorgs
                 ,'org_count':org_count
                 ,'conductor_count':conductor_count
                 ,'piece_count':piece_count
                 },
    )

def home(request):
    upcoming = []
    performances = PerformanceInstance.objects.all().filter(date__gte = datetime.date.today()).order_by('date')
    
    i = 0
    for prf in performances:
        upcoming.append(prf)

        i += 1
        if i == 4:
            break

    return render(
        request,
        'home.html',
        context={'upcoming':upcoming},
    )

def recordings(request):
    return render(
        request,
        'recordings.html',
        context={},
    )

def bio(request):
    return render(
        request,
        'bio.html',
        context={},
    )

def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')

            # Email the profile with the contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            send_mail('Message via peterlifland.com', content, contact_email, ['peter.lifland@gmail.com'], fail_silently=False)
            messages.success(request, 'Message sent. Thanks for contacting me!')
            return redirect('contact')

    return render(
        request,
        'contact.html',
        context={'form': form_class},
    )

def view_organizations(request):
    return render(
        request,
        'orglist.html',
        context={},
    )   

class OrganizationListView(generic.ListView):
    model = Organization
    template_name = 'orglist.html'
    
class OrganizationDetailView(generic.DetailView):
    #model = Organization
    context_object_name = 'orgdetail_list'
    template_name = 'orgdetail.html'
    
    def get_queryset(self):
        self.organization = get_object_or_404(Organization, id=self.kwargs.get('pk'))
        return Organization.objects.filter(id = self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        context['organization'] = Organization.objects.all()
        context['performance'] = Performance.objects.filter(organization = self.organization)
        # And so on for more models
        return context

### Autocomplete views
from dal import autocomplete
from django.db import models
from django.views import View
from django.http import JsonResponse

# organization-autocomplete/?q=b
class OrganizationAutocomplete(generic.View):
    def get(self, request):
        orgs = Organization.objects.all()

        q = self.request.GET.get('q')
        if q:
            orgs = orgs.filter(name__istartswith=q)

        orgs = orgs.values('id').annotate(maxyear=Max('organizationinstance__year'))
        organizationinstances = OrganizationInstance.objects.filter(Q(organization__in=[o['id'] for o in orgs]) & Q(year__in=[o['maxyear'] for o in orgs]))

        results = []
        for org in organizationinstances:
            results.append({ 'id':org.organization.pk, 'text':'{name}<br />{city}<br />{conductors}'.format(name = org.organization.name, city = org.organization.city, conductors = ", ".join(s.person.get_full_name() for s in org.conductors.all()) ), 'selected_text':org.organization.name })

        outdict = { 'results':results, 'pagination': {'more':False} }
        return JsonResponse(outdict)

class ConductorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Country.objects.none()

        qs = Conductor.objects.all()

        if self.q:
            qs = qs.filter(person__lastname__istartswith=self.q)

        return qs

def organizationinstanceform(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OrganizationInstanceForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('home'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = OrganizationInstanceForm()

    context = {
        'form': form
    }

    return render(request, 'sampleform.html', context)