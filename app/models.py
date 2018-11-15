from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique instances
from django.utils import timezone

### People ###
# Base class
class Person(models.Model):
    """ Model representing a human being """
    lastname = models.CharField(max_length=200, help_text="Enter a surname")
    firstname = models.CharField(max_length=200, help_text="Enter the rest of the name")
    
    def __str__(self):
        return '{0}, {1}'.format(self.lastname, self.firstname)
        
    def get_full_name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)

    class Meta:
        ordering = ["lastname","firstname"]

# Roles
class Administrator(models.Model):
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.person)

    class Meta:
        ordering = ["person"]

class Composer(models.Model):
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.person)

    class Meta:
        ordering = ["person"]
        
class Conductor(models.Model):
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.person)

    class Meta:
        ordering = ["person"]

class Singer(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    SOPRANO = 'S'
    MEZZO = 'M'
    ALTO = 'A'
    CONTRALTO = 'CA'
    COUNTERTENOR = 'CT'
    TENOR = 'T'
    BARITONE = 'BR'
    BASS = 'BS'
    UNKNOWN = 'U'
    VOICEPART_CHOICES = (
        (SOPRANO, 'Soprano'),
        (MEZZO, 'Mezzo'),
        (ALTO, 'Alto'),
        (CONTRALTO, 'Contralto'),
        (COUNTERTENOR, 'Countertenor'),
        (TENOR, 'Tenor'),
        (BARITONE, 'Baritone'),
        (BASS, 'Bass'),
        (UNKNOWN, 'Unknown/Other'),
    )
    voicepart = models.CharField(max_length=2, choices=VOICEPART_CHOICES, default=UNKNOWN)
    
    def __str__(self):
        return str(self.person)

    class Meta:
        ordering = ["person"]

### Groups ###
# Base class - immutable information, if one of these changes, it's a new group!
class Organization(models.Model):
    """ Model representing a singing ensemble/organization """
    name = models.CharField(max_length=200, help_text="Enter an organization name")

    COMMUNITY = 'CM'
    CHURCH = 'CH'
    PROFESSIONAL = 'PR'
    SCHOOL = 'SC'
    UNKNOWN = 'U'
    TYPE_CHOICES = (
        (COMMUNITY, 'Community Chorus'),
        (CHURCH, 'Church Choir'),
        (PROFESSIONAL, 'Professional'),
        (SCHOOL, 'School'),
        (UNKNOWN, 'Unknown/Other'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=UNKNOWN, help_text="Choose an organization type")

    CHAMBER = 'C'
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    UNKNOWN = 'U'
    SIZE_CHOICES = (
        (CHAMBER, 'Chamber (2-12 voices)'),
        (SMALL, 'Small (12-24 voices)'),
        (MEDIUM, 'Medium (24-50 voices)'),
        (LARGE, 'Large (50+ voices)'),
        (UNKNOWN, 'Unknown/Other'),
    )
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default=UNKNOWN, help_text="Choose an organization size")

    city = models.CharField(max_length=200, default="Unknown", help_text="Enter an organization city ([City, State] preferred)")
    url = models.URLField(max_length=200, default="Unknown", help_text="Enter an organization url")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization-detail', args=[str(self.id)])

    class Meta:
        ordering = ["name"]

# Instance, generally expect one per year
# Invoke the most recent per organization to fill out the base attributes
class OrganizationInstance(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    conductors = models.ManyToManyField(Conductor, related_name='conductor_primary', help_text='Primary conductor(s)', blank=True)
    associateconductors = models.ManyToManyField(Conductor, related_name='conductor_associate', help_text='Associate and assistant conductor(s)', blank=True)
    administrators = models.ManyToManyField(Administrator, help_text='Administrators and managers', blank=True)
    singerspaid = models.ManyToManyField(Singer, related_name='singer_paid', help_text='Paid singers and section leaders', blank=True)
    singersvolunteer = models.ManyToManyField(Singer, related_name='singer_volunteer', help_text='Volunteer singers', blank=True)
    
    def __str__(self):
        conductors_str = ", ".join(s.person.lastname for s in self.conductors.all())
        return '{0} {1:%b %Y}-{2:%b %Y} ({3})'.format(self.organization, self.start, self.end, conductors_str)
        
    class Meta:
        ordering = ["organization","-end"]


### Peformances and recordings ###
# Base class, not much here
class Performance(models.Model):
    name = models.CharField(max_length=200, help_text="Enter an performance/recording name")
    
    PERFORMANCE = 'P'
    RECORDING = 'R'
    SERVICE = 'S'
    TYPE_CHOICES = (
        (PERFORMANCE, 'Performance'),
        (RECORDING, 'Recording'),
        (SERVICE, 'Service'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=PERFORMANCE, help_text="Choose a performance type")
    
    def __str__(self):
        return '{0}: {1}'.format(self.get_type_display(), self.name)

class PerformanceInstance(models.Model):
    performance = models.ForeignKey('Performance', on_delete=models.SET_NULL, null=True)
    organizations = models.ManyToManyField(OrganizationInstance, help_text='Organization(s)')
    venue = models.CharField(max_length=200, default="Unknown", help_text="Enter an concert venue")
    city = models.CharField(max_length=200, default="Unknown", help_text="Enter the concert ([city, state] preferred)")
    date = models.DateField(null=False, blank=False)
    
    def __str__(self):
        return '{0} - {1} - {2}'.format(self.performance.name, self.date, self.venue)

    def was_this_year(self):
        now = timezone.now()
        if now.year ==  self.date.year:
            return True
        else:
            return False
        
    class Meta:
        ordering = ["-date","city","venue"]

class PerformancePiece(models.Model):
    performanceinstance = models.ForeignKey('PerformanceInstance', on_delete=models.SET_NULL, null=True)
    organizations = models.ManyToManyField(OrganizationInstance, help_text='Organization(s)')
    composition = models.ForeignKey('Composition', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return '{0} - {1}'.format(self.composition.title, self.performanceinstance.performance.name)
        
    class Meta:
        ordering = ["performanceinstance","composition"]

### Works of music ###
# Genre tags
class Genre(models.Model):
    """ Model representing a piece of music """
    ERA = 'E'
    SUBJECT = 'S'
    FORM = 'F'
    REGION = 'R'
    STYLE = 'Y'
    SUBTYPE_CHOICES = (
        (ERA, 'Era'),
        (SUBJECT, 'Subject'),
        (FORM, 'Form'),
        (REGION, 'Region'),
        (STYLE, 'Style'),
    )
    subtype = models.CharField(max_length=1, choices=SUBTYPE_CHOICES)
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return '{0}: {1}'.format(self.get_subtype_display(), self.name)
        
    class Meta:
        ordering = ["subtype","name"]

# Base class
class Composition(models.Model):
    """ Model representing a piece of music """
    title = models.CharField(max_length=200)
    composer = models.ForeignKey('Composer', related_name='composer', on_delete=models.SET_NULL, null=True)
    arranger = models.ForeignKey('Composer', related_name='arranger', on_delete=models.SET_NULL, null=True)
    year = models.PositiveIntegerField(blank=True)

    ACAPPELLA = 'AC'
    PIANO = 'PI'
    ORGAN = 'OG'
    PERCUSSION = 'PE'
    ORCHESTRA = 'OR'
    BRASS = 'BR'
    STRINGS = 'ST'
    CONTINUO = 'BC'
    BASS = 'BA'
    BELLS = 'BE'
    CELLO = 'CE'
    CLARINET = 'CL'
    GUITAR = 'GU'
    HARP = 'HP'
    TRUMPET = 'TR'
    VIOLIN = 'VI'
    WATERGLASS = 'WG'
    ACCOMPANIMENT_CHOICES = (
        (ACAPPELLA, 'A cappella'),
        (PIANO, 'Piano'),
        (ORGAN, 'Organ'),
        (PERCUSSION, 'Percussion'),
        (ORCHESTRA, 'Orchestra'),
        (BRASS, 'Brass'),
        (STRINGS, 'Strings'),
        (CONTINUO, 'Continuo'),
        (BASS, 'Bass'),
        (BELLS, 'Bells'),
        (CELLO, 'Cello'),
        (CLARINET, 'Clarinet'),
        (GUITAR, 'Guitar'),
        (HARP, 'Harp'),
        (TRUMPET, 'Trumpet'),
        (VIOLIN, 'Violin'),
        (WATERGLASS, 'Water Glasses'),
    )
    accompaniment = models.CharField(max_length=2, choices=ACCOMPANIMENT_CHOICES, default=ACAPPELLA)

    UNISON = 'U'
    SA = 'SA'
    SATB = 'MI'
    TB = 'TB'
    VOICING_CHOICES = (
        (UNISON, 'Unison'),
        (SA, 'SA'),
        (SATB, 'SATB'),
        (TB, 'TB'),
    )
    voicing = models.CharField(max_length=2, choices=VOICING_CHOICES, default=SATB)
    tags = models.ManyToManyField(Genre)
    
    AFRIKAANS = 'AF'
    ARABIC = 'AR'
    CATALAN = 'CA'
    CHINESE = 'ZH'
    CZECH = 'CS'
    DANISH = 'DA'
    DUTCH = 'NL'
    ENGLISH = 'EN'
    FINNISH = 'FI'
    FRENCH = 'FR'
    GEORGIAN = 'KA'
    GERMAN = 'DE'
    GREEK = 'EL'
    HEBREW = 'HE'
    HINDI = 'HI'
    HUNGARIAN = 'HU'
    ICELANDIC = 'IS'
    IRISH = 'GA'
    ITALIAN = 'IT'
    JAPANESE = 'JA'
    KOREAN = 'KO'
    LATIN = 'LA'
    NORWEGIAN = 'NO'
    POLISH = 'PL'
    PORTUGUESE = 'PR'
    RUSSIAN = 'RU'
    SLAVONIC = 'CU'
    SPANISH = 'ES'
    SWAHILI = 'SW'
    SWEDISH = 'SV'
    THAI = 'TH'
    TURKISH = 'TR'
    WELSE = 'CY'
    YIDDISH = 'YI'
    UNKNOWN = 'U'
    LANGUAGE_CHOICES = (
        (ENGLISH, 'English'),
        (LATIN, 'Latin'),
        (AFRIKAANS, 'Afrikaans'),
        (ARABIC, 'Arabic'),
        (CATALAN, 'Catalan'),
        (CHINESE, 'Chinese (all)'),
        (CZECH, 'Czech'),
        (DANISH, 'Danish'),
        (DUTCH, 'Dutch'),
        (FINNISH, 'Finnish'),
        (FRENCH, 'French'),
        (GEORGIAN, 'Georgian'),
        (GERMAN, 'German'),
        (GREEK, 'Greek (all)'),
        (HEBREW, 'Hebrew'),
        (HINDI, 'Hindi'),
        (HUNGARIAN, 'Hungarian'),
        (ICELANDIC, 'Icelandic'),
        (IRISH, 'Irish and Gaelic'),
        (ITALIAN, 'Italian'),
        (JAPANESE, 'Japanese'),
        (KOREAN, 'Korean'),
        (NORWEGIAN, 'Norwegian'),
        (POLISH, 'Polish'),
        (PORTUGUESE, 'Portuguese'),
        (RUSSIAN, 'Russian'),
        (SLAVONIC, 'Slavonic (all)'),
        (SPANISH, 'Spanish'),
        (SWAHILI, 'Swahili'),
        (SWEDISH, 'Swedish'),
        (THAI, 'Thai'),
        (TURKISH, 'Turkish'),
        (WELSE, 'Welsh'),
        (YIDDISH, 'Yiddish'),
        (UNKNOWN, 'Unknown/Other'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=ENGLISH)
    
    def __str__(self):
        return '{0} - {1}'.format(self.composer, self.title)
        
    class Meta:
        ordering = ["composer","title"]