from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('recordings', views.recordings, name='recordings'),
    path('bio', views.bio, name='bio'),
    path('contact', views.contact, name='contact'),
    path('vocalcv', views.vocalcv, name='vocalcv'),
    path('organizations/', views.OrganizationListView.as_view(), name='organizations'),
    path('organization/<int:pk>', views.OrganizationDetailView.as_view(), name='organization-detail'),

    re_path(r'^organization-autocomplete/$', views.OrganizationAutocomplete.as_view(), name='organization-autocomplete'),
    re_path(r'^conductor-autocomplete/$', views.ConductorAutocomplete.as_view(), name='conductor-autocomplete'),
    path('organizationinstanceform', views.organizationinstanceform, name='organizationinstanceform'),
]