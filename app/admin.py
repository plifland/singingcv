from django.contrib import admin

# Register your models here.
from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance, Performance, PerformanceInstance, PerformancePiece, Composition, Genre
from .forms import *
admin.site.register(Person)
admin.site.register(Administrator)
admin.site.register(Conductor)
admin.site.register(Singer)
admin.site.register(Organization)
admin.site.register(Performance)
admin.site.register(PerformanceInstance)
admin.site.register(PerformancePiece)

class ComposerAdmin(admin.ModelAdmin):
    form = ComposerForm
admin.site.register(Composer, ComposerAdmin)

class CompositionAdmin(admin.ModelAdmin):
    form = CompositionForm
admin.site.register(Composition, CompositionAdmin)

class GenreAdmin(admin.ModelAdmin):
    form = GenreForm
admin.site.register(Genre, GenreAdmin)

class OrganizationInstanceAdmin(admin.ModelAdmin):
    form = OrganizationInstanceForm
admin.site.register(OrganizationInstance, OrganizationInstanceAdmin)