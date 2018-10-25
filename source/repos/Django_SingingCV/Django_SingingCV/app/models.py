from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique instances

# Create your models here.
class Composition(models.Model):
    """ Model representing a piece of music """
    title = models.CharField(max_length=200, help_text="Enter a piece title")
    composer = models.ForeignKey('Composer', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return '{0} - {1}'.format(self.composer, self.title)
        
    class Meta:
        ordering = ["composer","title"]
        
class Person(models.Model):
    """ Model representing a human being """
    lastname = models.CharField(max_length=200, help_text="Enter a surname")
    firstname = models.CharField(max_length=200, help_text="Enter the rest of the name")
    
    def __str__(self):
        return '{0}, {1}'.format(self.lastname, self.firstname)
        
    def get_full_name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)
        
class Composer(models.Model):
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.person.lastname
        
class Conductor(models.Model):
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.person.lastname

class Singer(models.Model):
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True)
    voicepart = models.CharField(max_length=40, help_text="Enter a voice part")
    
    def __str__(self):
        return self.person

class Organization(models.Model):
    """ Model representing a singing ensemble/organization """
    name = models.CharField(max_length=200, help_text="Enter an organization name")
    type = models.CharField(max_length=40, help_text="Enter an organization type")
    size = models.CharField(max_length=40, help_text="Enter an organization size")
    url = models.CharField(max_length=200, help_text="Enter an organization url")
    conductor = models.ForeignKey('Conductor', on_delete=models.SET_NULL, null=True)
    #hourlypay = 
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('organization-detail', args=[str(self.id)])
        
class PerformanceInstance(models.Model):
    """ Model representing a singing performance date """
    venue = models.CharField(max_length=200, help_text="Enter an concert venue")
    city = models.CharField(max_length=200, help_text="Enter the concert city, state", null=True)
    date = models.DateField(null=False, blank=False)
    
    def __str__(self):
        return '{0} - {1}'.format(self.date, self.venue)
        
    class Meta:
        ordering = ["-date","city","venue"]
        
class Performance(models.Model):
    """ Model representing a singing performance group """
    name = models.CharField(max_length=200, help_text="Enter an concert name")
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    performances = models.ManyToManyField(PerformanceInstance, help_text='When/where was this performance?')
    pieces = models.ManyToManyField(Composition, help_text='What pieces were in this concert?')
    
    def __str__(self):
        return '{0} - {1}'.format(self.organization, self.name)
        
class Recording(models.Model):
    """ Model representing a singing recording """
    name = models.CharField(max_length=200, help_text="Enter an recording name")
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    venue = models.CharField(max_length=200, help_text="Enter an recording venue")
    url = models.CharField(max_length=200, help_text="Enter an recording link")
    date = models.DateField(null=False, blank=False)
    pieces = models.ManyToManyField(Composition, help_text='What pieces were in this concert?')
    
    def __str__(self):
        return '{0} - {1}'.format(self.organization, self.name)