import datetime

from django.db.models import Max,Q,Count
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.views import generic
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import date
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance, Performance, PerformanceInstance, PerformancePiece, Composition, Genre
from .forms import ContactForm, GenreForm, OrganizationInstanceForm, CompositionForm, ComposerForm, RepListFiltersForm

@login_required
def vocalcv(request):
    # Find me as a singer!
    me_singer = Singer.objects.get(Q(person__firstname = 'Peter') & Q(person__lastname = 'Lifland'))
    me_singer_pk = me_singer.pk

    # My organizations
    organizationinstances = OrganizationInstance.objects.all()
    me_organizationinstances = list(chain(organizationinstances.filter(singerspaid=me_singer_pk).values_list('id', flat=True), organizationinstances.filter(singersvolunteer=me_singer_pk).values_list('id', flat=True)))

    # Gets the most recent record per organization
    orgs = Organization.objects.values('id').annotate(maxdate=Max('organizationinstance__start'))
    q = [Q(organization=o['id']) & Q(start=o['maxdate']) for o in orgs]
    mru_organizationinstances = organizationinstances.filter(reduce(OR, q))

    # Let's add a filter for upcoming performances
    performances = PerformanceInstance.objects.all().filter(date__gte = datetime.date.today())
    #performance_orgs = []
    #for prf in performances:
    #    for org in prf.organizations.all():
    #        performance_orgs.append(org.organization.id)
    #performance_orgs = list(set(performance_orgs))
    performance_orgs = list(set(performances.values_list('organizations__organization', flat=True)))
    activeorgs = mru_organizationinstances.filter(Q(organization__in=performance_orgs) & Q(pk__in=me_organizationinstances))
    inactiveorgs = mru_organizationinstances.filter(pk__in=me_organizationinstances).exclude(pk__in=activeorgs)

    me_org_count = organizationinstances.filter(pk__in=me_organizationinstances).values('organization').distinct().count()
    me_conductor_count = organizationinstances.filter(pk__in=me_organizationinstances).values('conductors').distinct().count()
    me_piece_count = Composition.objects.filter(performancepiece__organizations__in=me_organizationinstances).distinct().count()

    db_org_count = Organization.objects.count()
    db_conductor_count = Conductor.objects.count()
    db_piece_count = Composition.objects.count()
    
    return render(
        request,
        'vocalcv.html',
        context={
            'activeorgs':activeorgs,
            'inactiveorgs':inactiveorgs,
            'me_org_count':me_org_count,
            'me_conductor_count':me_conductor_count,
            'me_piece_count':me_piece_count,
            'db_org_count':db_org_count,
            'db_conductor_count':db_conductor_count,
            'db_piece_count':db_piece_count,
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

def links(request):
    return render(
        request,
        'links.html',
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

class Performances(LoginRequiredMixin, generic.View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return Performance.objects.none()

        # Gets the most recent record per organization
        #performances = Performance.objects.all()
        performanceinstances = PerformanceInstance.objects.all()
    
        return render(
            request,
            'performances.html',
            context={'performanceinstances':performanceinstances},
        )
class PerformancesSpecific(LoginRequiredMixin, generic.View):
    def get(self, request, pk, pi):
        if not self.request.user.is_authenticated:
            return Performance.objects.none()

        # Gets the most recent record per organization
        #performances = Performance.objects.all()
        performanceinstances = PerformanceInstance.objects.all()
    
        context={
            'performanceinstances':performanceinstances,
            'pk':pk,
            'pi':pi,
            }
        return render(
            request,
            'performances.html',
            context,
        )
@login_required
def performance_detail(request, pk):
    performance = Performance.objects.get(pk=pk)
    performanceinstances = PerformanceInstance.objects.filter(performance=pk)
    return render(
        request,
        'performancedetails.html',
        {'performance':performance, 'performanceinstances':performanceinstances},
    )
@login_required
def performance_pieces(request, pk):
    pieces = PerformancePiece.objects.filter(performanceinstance=pk)

    pieces_grouped = {}
    for p in pieces:
        for oi in p.organizations.all():
            if not oi.organization.name in pieces_grouped:
                pieces_grouped[oi.organization.name] = {}
            pieces_grouped[oi.organization.name][p.composition.pk] = p

    return render(
        request,
        'performancepieces.html',
        {'pieces':pieces_grouped},
    )
@login_required
def performance_pieces_all(request, pk):
    pieces = PerformancePiece.objects.filter(performanceinstance__performance=pk)

    pieces_grouped = {}
    for p in pieces:
        for oi in p.organizations.all():
            if not oi.organization.name in pieces_grouped:
                pieces_grouped[oi.organization.name] = {}
            pieces_grouped[oi.organization.name][p.composition.pk] = p

    return render(
        request,
        'performancepieces.html',
        {'pieces':pieces_grouped},
    )

@login_required
def rep_list(request):
    # Find me as a singer!
    me_singer = Singer.objects.get(Q(person__firstname = 'Peter') & Q(person__lastname = 'Lifland'))
    me_singer_pk = me_singer.pk

    # My organizations
    me_organizationinstances = OrganizationInstance.objects.filter(Q(singerspaid=me_singer_pk) | Q(singersvolunteer=me_singer_pk))

    pieces = PerformancePiece.objects.filter(organizations__in=me_organizationinstances)

    ### Filters
    composer = request.GET.get('composer')
    if composer:
        try:
            composerint = int(composer)
            pieces = pieces.filter(composition__composer=composer)
        except:
            ## Hopefully we have a "Lastname, Firstname" string at this point
            try:
                (lastname, firstname) = composer.split(', ')
                #firstname = firstname[1:] # remove the space
                pieces = pieces.filter(Q(composition__composer__person__firstname=firstname) & Q(composition__composer__person__lastname=lastname))
            except ValueError:
                pieces = pieces
    org = request.GET.get('org')
    if org:
        pieces = pieces.filter(organizations__organization=org)
    year = request.GET.get('year')
    if year:
        pieces = pieces.filter(performanceinstance__date__year=year)
    era = request.GET.get('era')
    if era:
        pieces = pieces.filter(composition__tags=era)

    piecesdict = {}
    for p in pieces:
        # New piece
        if not p.composition.pk in piecesdict:
            performances = {}
            piecesdict[p.composition.pk] = {'composer':str(p.composition.composer), 'title':p.composition.title, 'performances':performances}
        # Add on performances - will dedupe later!
        for o in p.organizations.all():
            if o.organization.pk in piecesdict[p.composition.pk]['performances']:
                piecesdict[p.composition.pk]['performances'][o.organization.name].append(p.performanceinstance.date.year)
                piecesdict[p.composition.pk]['performances'][o.organization.name] = sorted(set(piecesdict[p.composition.pk]['performances'][o.organization.pk]))
            else:
                piecesdict[p.composition.pk]['performances'][o.organization.name] = [p.performanceinstance.date.year]

    sorteddict = sorted(piecesdict.items(), key = lambda v: (v[1]['composer'], v[1]['title']))

    paginator = Paginator(sorteddict, 20) # Show 20 pieces per page
    page = request.GET.get('page')
    pieces_page = paginator.get_page(page)

    form = RepListFiltersForm

    return render(
        request,
        'replist.html',
        {
            'pieces':pieces_page
            ,'form':form
         },
    )

from itertools import chain
@login_required
def org_details(request, pk):
    org = pk
    try:
        pk = int(org)
    except:
        ## This means we were passed an orgname
        try:
            pk = Organization.objects.get(name=org).pk
        except ValueError:
            return

    # Get the most recent organizationinstance per org
    organizationinstances = OrganizationInstance.objects.filter(organization=pk)
    orgstart = Organization.objects.filter(pk=pk).values('id').annotate(maxyear=Max('organizationinstance__start'))
    q = [Q(organization=o['id']) & Q(start=o['maxyear']) for o in orgstart]
    organizationinstance_mostrecent = organizationinstances.get(reduce(OR, q))

    sopranos = list(chain(organizationinstance_mostrecent.singerspaid.filter(Q(voicepart='S') | Q(voicepart='M')), organizationinstance_mostrecent.singersvolunteer.filter(Q(voicepart='S') | Q(voicepart='M'))))
    altos = list(chain(organizationinstance_mostrecent.singerspaid.filter(Q(voicepart='A') | Q(voicepart='CT')), organizationinstance_mostrecent.singersvolunteer.filter(Q(voicepart='A') | Q(voicepart='CT'))))
    tenors = list(chain(organizationinstance_mostrecent.singerspaid.filter(Q(voicepart='T') | Q(voicepart='CA')), organizationinstance_mostrecent.singersvolunteer.filter(Q(voicepart='T') | Q(voicepart='CA'))))
    basses = list(chain(organizationinstance_mostrecent.singerspaid.filter(Q(voicepart='BR') | Q(voicepart='BS')), organizationinstance_mostrecent.singersvolunteer.filter(Q(voicepart='BR') | Q(voicepart='BS'))))
    
    performances = PerformanceInstance.objects.filter(organizations__in=[o.pk for o in organizationinstances])

    context = {
        'orginst_mostrecent':organizationinstance_mostrecent,
        'sopranos':sopranos,
        'altos':altos,
        'tenors':tenors,
        'basses':basses,
        'performances':performances
        }
    return render(request, 'orgdetail.html', context)

class OrganizationListView(LoginRequiredMixin, generic.ListView):
    model = Organization
    template_name = 'orglist.html'
#class OrganizationDetailView(generic.DetailView):
#    #model = Organization
#    context_object_name = 'orgdetail_list'
#    template_name = 'orgdetail.html'
    
#    def get_queryset(self):
#        self.organization = get_object_or_404(Organization, id=self.kwargs.get('pk'))
#        return Organization.objects.filter(id = self.kwargs.get('pk'))
    
#    def get_context_data(self, **kwargs):
#        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
#        context['organization'] = Organization.objects.all()
#        context['performance'] = Performance.objects.filter(organization = self.organization)
#        # And so on for more models
#        return context

### Autocomplete views
from dal import autocomplete
from django.db import models
from django.views import View
from django.http import JsonResponse
from functools import reduce
from operator import __or__ as OR
from django.db.models import CharField, Value
from django.db.models.functions import Concat

### Self-written autocomplete url - responds to a url with a list of organizations formatted in JSON for the DAL (django autocomplete light) views
### Example testing url: organization-autocomplete/?q=b
class OrganizationAutocomplete(generic.View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return Organization.objects.none()

        # Get the base object
        orgs = Organization.objects.all()

        # Filter based on name
        q = self.request.GET.get('q')
        if q:
            orgs = orgs.filter(name__istartswith=q)

        # Organization needs to be crossed with an organizationinstance
        # This code gets the most recent organizationinstance per organization (post org filtering from above)
        orgs = orgs.values('id').annotate(maxyear=Max('organizationinstance__start'))
        #organizationinstances = OrganizationInstance.objects.filter(Q(organization__in=[o['id'] for o in orgs]) & Q(start__in=[o['maxyear'] for o in orgs]))
        q = [Q(organization=o['id']) & Q(start=o['maxyear']) for o in orgs]
        organizationinstances = OrganizationInstance.objects.filter(reduce(OR, q))

        # Create the results block, which is a list of JSON objects as follows
        # Format: [{id, text, selected_text},...]
        #   id              pk of the object selected
        #   text            text of the autocomplete suggestion, formatted as html
        #   selected_text   text of the filled auto-complete (after a selection by the user)
        results = []
        for org in organizationinstances:
            results.append({ 
                'id':org.organization.pk,
                 'text':'<span class="autocomplete-main">{name}</span><div class="autocomplete-detail">last updated {year}</div><div class="autocomplete-detail">{city}</div><div class="autocomplete-detail">{conductors}</div>'.format(
                     name = org.organization.name,
                     year = "{0:%b %Y}".format(org.end),
                     city = org.organization.city,
                     conductors = "<br />".join(s.person.get_full_name() for s in org.conductors.all()),
                     ),
                 'selected_text':org.organization.name,
                 })

        # Add on orgs that have no instance
        orgs = Organization.objects.filter(organizationinstance__isnull=True)
        for org in orgs:
            results.append({
                'id':org.pk,
                'text':org.name,
                'selected_text':org.name,

                })

        # Format: { results : [{id, text, selected_text},...], pagination : { more : BOOL } }
        outdict = { 'results':results, 'pagination':{'more':False} }

        return JsonResponse(outdict)
class OrganizationInstanceAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return '<span class="autocomplete-main">{name}</span><div class="autocomplete-detail">{start} - {end}</div>'.format(
            name = item.organization.name,
            start = item.start,
            end = item.end,
            )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return OrganizationInstance.objects.none()

        qs = OrganizationInstance.objects.all()

        # Fetch an performance to filter with, if we can
        perfinst = self.forwarded.get('performanceinstance', None)

        # organizationinstance-autocomplete/?performanceinstance=2
        if perfinst:
            performance = PerformanceInstance.objects.filter(pk = perfinst)
            if performance:
                qs = qs.filter(id__in = [o.id for o in performance.first().organizations.all()])

        if self.q:
            qs = qs.filter(organization__name__contains=self.q)

        return qs
class PersonAutocomplete(generic.View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return Person.objects.none()

        persons = Person.objects.all()

        q = self.request.GET.get('q')
        if q:
            persons = persons.annotate(fullname=Concat('firstname', Value(' '), 'lastname', output_field=CharField())).filter(fullname__icontains=q)

        results = []
        for p in persons:
            singer = Singer.objects.filter(person=p.pk)
            if singer:
                singertext = "Singer ({0})".format(", ".join(s.get_voicepart_display() for s in singer))
            else:
                singertext = ""

            composer = Composer.objects.filter(person=p.pk)
            if composer:
                composertext = "Composer"
            else:
                composertext = ""

            try:
                conductor = Conductor.objects.get(person=p.pk)
            except Conductor.DoesNotExist:
                conductor = None
            if conductor:
                orgs = OrganizationInstance.objects.filter(Q(conductors = conductor.pk) | Q(associateconductors = conductor.pk))
                if orgs:
                    orgs = list(set(orgs.values_list('organization__name', flat=True)))[:3]
                    conductortext = "Conductor ({0})".format(", ".join(o for o in orgs))
                else:
                    conductortext = "Conductor"
            else:
                conductortext = ""

            try:
                admin = Administrator.objects.get(person=p.pk)
            except Administrator.DoesNotExist:
                admin = None
            if admin:
                orgs = OrganizationInstance.objects.filter(administrators = admin.pk)
                if orgs:
                    orgs = list(set(orgs.values_list('organization__name', flat=True)))[:3]
                    admintext = "Administrator ({0})".format(", ".join(o for o in orgs))
                else:
                    admintext = "Administrator"
            else:
                admintext = ""

            results.append({
                'id':p.pk,
                 'text':'''<span class="autocomplete-main">{name}</span>
                            <div class="autocomplete-detail">{singer}</div>
                            <div class="autocomplete-detail">{conductor}</div>
                            <div class="autocomplete-detail">{administrator}</div>
                            <div class="autocomplete-detail">{composer}</div>'''.format(
                     name = p.get_full_name(),
                     singer = singertext,
                     conductor = conductortext,
                     administrator = admintext,
                     composer = composertext,
                     ),
                 'selected_text':'{name}'.format(
                     name = p.get_full_name(),
                     ),
                 })


        # Format: { results : [{id, text, selected_text},...], pagination : { more : BOOL } }
        outdict = { 'results':results, 'pagination':{'more':False} }

        return JsonResponse(outdict)
class AdministratorAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.person.get_full_name()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Administrator.objects.none()

        qs = Administrator.objects.all()

        if self.q:
            qs = qs.filter(Q(person__lastname__istartswith=self.q) | Q(person__firstname__istartswith=self.q))

        return qs
class ComposerAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.person.get_full_name()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Composer.objects.none()

        qs = Composer.objects.all()

        if self.q:
            qs = qs.filter(Q(person__lastname__istartswith=self.q) | Q(person__firstname__istartswith=self.q))

        return qs
class ConductorAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.person.get_full_name()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Conductor.objects.none()

        qs = Conductor.objects.all()

        if self.q:
            qs = qs.filter(Q(person__lastname__istartswith=self.q) | Q(person__firstname__istartswith=self.q))

        return qs
class SingerAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return '{name} ({voicepart})'.format(
            name = item.person.get_full_name(),
            voicepart = item.get_voicepart_display(),
            )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Singer.objects.none()

        qs = Singer.objects.all()

        if self.q:
            qs = qs.filter(Q(person__lastname__istartswith=self.q) | Q(person__firstname__istartswith=self.q))

        return qs
class GenreAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Genre.objects.none()

        qs = Genre.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
class CompositionAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return '{title} ({voicing})<br />{composer} - {year}'.format(
            title = item.title,
            composer = item.composer,
            year = item.year,
            voicing = item.get_voicing_display(),
            )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Composition.objects.none()

        qs = Composition.objects.all()

        if self.q:
            qs = qs.filter(title__contains=self.q)

        return qs
class PerformanceAutocomplete(generic.View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return Performance.objects.none()

        qs = PerformanceInstance.objects.all()

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(performance__name__contains=q) | Q(performance__name__contains=q))

        performances = {}
        for p in qs:
            if not p.performance.pk in performances:
                orgs = []
                performances[p.performance.pk] = {'name': p.performance.name, 'orgs': orgs, 'firstdate': date(p.date.year, p.date.month, 1), 'lastdate':date(p.date.year, p.date.month, 1)}
            else:
                if (p.date < performances[p.performance.pk]['firstdate']):
                    performances[p.performance.pk]['firstdate'] = date(p.date.year, p.date.month, 1)
                elif (p.date > performances[p.performance.pk]['lastdate']):
                    performances[p.performance.pk]['lastdate'] = date(p.date.year, p.date.month, 1)
            for o in p.organizations.all():
                performances[p.performance.pk]['orgs'].append(o.organization.name)

        results = []
        for pk,v in performances.items():
            if (v['firstdate'] == v['lastdate']):
                datestr = "{start:%b %Y}".format(start = v['firstdate'])
            else:
                datestr = "{start:%b %Y} - {end:%b %Y}".format(start = v['firstdate'], end = v['lastdate'])
            results.append({
                'id':pk,
                 'text':'<span class="autocomplete-main">{name}</span><div class="autocomplete-detail">{orgs}</div><div class="autocomplete-detail">{dates}</div>'.format(
                     name = v['name'],
                     orgs = "<br />".join(s for s in sorted(set(v['orgs']))),
                     dates = datestr,
                     ),
                 'selected_text':'{name}'.format(
                     name = v['name'],
                     ),
                 })

        # Add on orgs that have no instance
        performances = Performance.objects.filter(performanceinstance__isnull=True)
        for p in performances:
            results.append({
                'id':p.pk,
                'text':'<span style="font-size:120%">{name}</span>'.format(name = p.name),
                'selected_text':p.name,
                })

        # Format: { results : [{id, text, selected_text},...], pagination : { more : BOOL } }
        outdict = { 'results':results, 'pagination':{'more':False} }

        return JsonResponse(outdict)
class PerformanceInstanceAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return '{title}<br />{orgs}<br />{date}'.format(
            title = item.performance.name,
            orgs = ", ".join(s.organization.name for s in item.organizations.all()),
            date = item.date,
            )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PerformanceInstance.objects.none()

        qs = PerformanceInstance.objects.all()

        if self.q:
            qs = qs.filter(performance__name__contains=self.q)

        return qs


### Forms
@login_required
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

@login_required
def compositionform(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CompositionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            entry = Composition.objects.create(
                title=form.cleaned_data['title'],
                composer=form.cleaned_data['composer'],
                year=form.cleaned_data['year'],
                accompaniment=form.cleaned_data['accompaniment'],
                voicing=form.cleaned_data['voicing'],
                tags=form.cleaned_data['tags'],
                language=form.cleaned_data['language'],
            )
            entry.save()
            return HttpResponseRedirect(reverse('compositionform'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CompositionForm()

    context = {
        'form': form
    }

    return render(request, 'sampleform.html', context)

@login_required
def composerform(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ComposerForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            entry = Composer.objects.create(
                person=form.cleaned_data['person'],
            )
            entry.save()
            return HttpResponseRedirect(reverse('composerform'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = ComposerForm()

    context = {
        'form': form
    }

    return render(request, 'forms/composer_create.html', context)

@login_required
def genreform(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = GenreForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            entry = Genre.objects.create(
                subtype=form.cleaned_data['subtype'],
                name=form.cleaned_data['name'],
            )
            entry.save()
            return HttpResponseRedirect(reverse('genreform'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = GenreForm()

    context = {
        'form': form
    }

    return render(request, 'sampleform.html', context)