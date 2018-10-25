from django.contrib import admin

# Register your models here.
from .models import Composition, Person, Composer, Conductor, Singer, Organization, PerformanceInstance, Performance, Recording
admin.site.register(Composition)
admin.site.register(Person)
admin.site.register(Composer)
admin.site.register(Conductor)
admin.site.register(Singer)
admin.site.register(Organization)
admin.site.register(PerformanceInstance)
admin.site.register(Performance)
admin.site.register(Recording)