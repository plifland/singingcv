from django.contrib import admin

# Register your models here.
from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance, Performance, PerformanceInstance, PerformancePiece, Composition, Genre
admin.site.register(Person)
admin.site.register(Administrator)
admin.site.register(Composer)
admin.site.register(Conductor)
admin.site.register(Singer)
admin.site.register(Organization)
admin.site.register(OrganizationInstance)
admin.site.register(Performance)
admin.site.register(PerformanceInstance)
admin.site.register(PerformancePiece)
admin.site.register(Composition)
admin.site.register(Genre)