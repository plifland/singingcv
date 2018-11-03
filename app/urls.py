from django.urls import path,re_path,include
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

    path('organizations/', views.OrganizationListView.as_view(), name='organizations'),
    path('organization/<int:pk>', views.OrganizationDetailView.as_view(), name='organization-detail'),

    path('accounts/', include('django.contrib.auth.urls')),

    re_path(r'^organization-autocomplete/$', views.OrganizationAutocomplete.as_view(), name='organization-autocomplete'),
    re_path(r'^conductor-autocomplete/$', views.ConductorAutocomplete.as_view(), name='conductor-autocomplete'),
    re_path(r'^administrator-autocomplete/$', views.AdministratorAutocomplete.as_view(), name='administrator-autocomplete'),
    re_path(r'^singer-autocomplete/$', views.SingerAutocomplete.as_view(), name='singer-autocomplete'),
    path('organizationinstanceform', views.organizationinstanceform, name='organizationinstanceform'),
]