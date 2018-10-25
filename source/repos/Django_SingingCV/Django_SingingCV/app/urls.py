from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('organizations/', views.OrganizationListView.as_view(), name='organizations'),
    path('organization/<int:pk>', views.OrganizationDetailView.as_view(), name='organization-detail'),
]