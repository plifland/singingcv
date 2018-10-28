import datetime

from django.db.models import Max,Q
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.views import generic

from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance, Performance, PerformanceInstance, PerformancePiece, Composition
    
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
    
    # Orgs with performances

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
    return render(
        request,
        'contact.html',
        context={},
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