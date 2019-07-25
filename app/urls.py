from django.urls import path,re_path,include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('recordings', views.recordings, name='recordings'),
    path('bio', views.bio, name='bio'),
    path('links', login_required(views.links), name='links'),
    path('contact', views.contact, name='contact'),
    path('vocalcv', views.vocalcv, name='vocalcv'),
    path('guestlogin', auth_views.LoginView.as_view(template_name='registration/login.html'), name='guestlogin'),

    path('performances', views.Performances.as_view(), name='performances'),
    path('performances?<int:pk>&<int:pi>', views.PerformancesSpecific.as_view(), name='performances-specific'),
    #path('performance-detail/<int:pk>', views.performance_detail, name='performance-detail'),
    path('performance-pieces/<int:pk>', views.performance_pieces, name='performance-pieces'),
    path('performance-pieces-all/<int:pk>', views.performance_pieces_all, name='performance-pieces-all'),

    path('services', views.Services.as_view(), name='services'),

    path('replist', views.rep_list, name='replist'),

    path('organizations/', views.OrganizationListView.as_view(), name='organizations'),
    path('organization/<int:pk>', views.org_details, name='organization-detail'),
    re_path(r'^organization/(?P<pk>[\w\s:\-]+)$', views.org_details, name='organization-detail-name'),
    path('composition/<int:pk>', views.composition_details, name='composition-detail'),

    path('accounts/', include('django.contrib.auth.urls')),

    re_path(r'^organization-autocomplete/$', views.OrganizationAutocomplete.as_view(), name='organization-autocomplete'),
    re_path(r'^person-autocomplete/$', views.PersonAutocomplete.as_view(), name='person-autocomplete'),
    re_path(r'^administrator-autocomplete/$', views.AdministratorAutocomplete.as_view(), name='administrator-autocomplete'),
    re_path(r'^composer-autocomplete/$', views.ComposerAutocomplete.as_view(), name='composer-autocomplete'),
    re_path(r'^conductor-autocomplete/$', views.ConductorAutocomplete.as_view(), name='conductor-autocomplete'),
    re_path(r'^singer-autocomplete/$', views.SingerAutocomplete.as_view(), name='singer-autocomplete'),
    re_path(r'^genre-autocomplete/$', views.GenreAutocomplete.as_view(), name='genre-autocomplete'),
    re_path(r'^composition-autocomplete/$', views.CompositionAutocomplete.as_view(), name='composition-autocomplete'),
    re_path(r'^performance-autocomplete/$', views.PerformanceAutocomplete.as_view(), name='performance-autocomplete'),
    re_path(r'^performanceinstance-autocomplete/$', views.PerformanceInstanceAutocomplete.as_view(), name='performanceinstance-autocomplete'),
    re_path(r'^organizationinstance-autocomplete/$', views.OrganizationInstanceAutocomplete.as_view(), name='organizationinstance-autocomplete'),

    path('organizationinstanceform', views.organizationinstanceform, name='organizationinstanceform'),
    path('compositionform', views.compositionform, name='compositionform'),
    path('composerform', views.composerform, name='composerform'),
    path('genreform', views.genreform, name='genreform'),
]