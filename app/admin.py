from django.contrib import admin

# Register your models here.
from .models import Person, Administrator, Composer, Conductor, Singer, Organization, OrganizationInstance, Performance, PerformanceInstance, PerformancePiece, Composition, Genre
from .forms import *
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Performance)

class AdministratorAdmin(admin.ModelAdmin):
    form = AdministratorForm
admin.site.register(Administrator, AdministratorAdmin)

class ComposerAdmin(admin.ModelAdmin):
    form = ComposerForm
admin.site.register(Composer, ComposerAdmin)

class CompositionAdmin(admin.ModelAdmin):
    form = CompositionForm
admin.site.register(Composition, CompositionAdmin)

class ConductorAdmin(admin.ModelAdmin):
    form = ConductorForm
admin.site.register(Conductor, ConductorAdmin)

class GenreAdmin(admin.ModelAdmin):
    form = GenreForm
admin.site.register(Genre, GenreAdmin)

class OrganizationInstanceAdmin(admin.ModelAdmin):
    form = OrganizationInstanceForm
admin.site.register(OrganizationInstance, OrganizationInstanceAdmin)

class PerformanceInstanceAdmin(admin.ModelAdmin):
    form = PerformanceInstanceForm
admin.site.register(PerformanceInstance, PerformanceInstanceAdmin)

class PerformancePieceAdmin(admin.ModelAdmin):
    form = PerformancePieceForm
    save_as = True
admin.site.register(PerformancePiece, PerformancePieceAdmin)

class SingerAdmin(admin.ModelAdmin):
    form = SingerForm
admin.site.register(Singer, SingerAdmin)
