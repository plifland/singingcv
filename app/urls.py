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
]