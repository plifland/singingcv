from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.views import generic

from .models import Composition, Person, Composer, Conductor, Singer, Organization, PerformanceInstance, Performance, Recording

# def index(request):
    # """ View function for home page of site """
    # # Generate counts of some of the main objects
    # num_organizations = Organization.objects.count()
    # num_conductors = Conductor.objects.count()
    # num_pieces = Composition.objects.count()
    
    # # Render the HTML template index.html with the data in the context variable
    # return render(
        # request,
        # 'index.html',
        # context={'num_organizations':num_organizations,'num_conductors':num_conductors,'num_pieces':num_pieces},
    # )
    
# def index(request):
    # performances = Performance.objects.all()
    # organizations = Organization.objects.all()
    
    # return render(
        # request,
        # 'index.html',
        # context={'performances':performances,'organizations':organizations},
    # )
    
def vocalcv(request):
    performancesbyyear = {}
    performances = Performance.objects.all()
    organizations = Organization.objects.all()
    
    for performance_group in performances:
        for performance_inst in performance_group.performances.all():
            year_key = performance_inst.date.year
            if not year_key in performancesbyyear:
                performancesbyyear[year_key] = {'year': year_key, 'organizations': []}
            if not performance_group.organization in performancesbyyear[year_key]['organizations']:
                performancesbyyear[year_key]['organizations'].append(performance_group.organization)
    
    return render(
        request,
        'vocalcv.html',
        context={'performancesbyyear':performancesbyyear,'performances':performances,'organizations':organizations},
    )

def home(request):
    return render(
        request,
        'home.html',
        context={},
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