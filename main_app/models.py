from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from phone_field import PhoneField

STATES = (
    ('AL', 'Alabama'),('AK', 'Alaska'),('AS', 'American Samoa'),
    ('AZ', 'Arizona'),('AR', 'Arkansas'),('CA', 'California'),
    ('CO', 'Colorado'),('CT', 'Connecticut'),('DR', 'Deleware'),
    ('DC', 'District of Columbia'),('FL', 'Florida'),('GA', 'Georgia'),
    ('GU', 'Guam'),('HI', 'Hawaii'),('ID', 'Idaho'),
    ('IL', 'Illinois'),('IN', 'Indiana'),('IA', 'Iowa'),
    ('KS', 'Kansas'),('KY', 'Kentucky'),('LA', 'Louisiana'),
    ('ME', 'Maine'),('MD', 'Maryland'),('MA', 'Massachusetts'),
    ('MI', 'Michigan'),('MN', 'Minnesota'),('MS', 'Mississippi'),
    ('MO', 'Missouri'),('MT', 'Montana'),('NE', 'Nebraska'),
    ('NV', 'Nevada'),('NH', 'New Hampshire'),('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),('NY', 'New York'),('NC', 'North Carolina'),
    ('ND', 'North Dakota'),('OH', 'Ohio'),('OK', 'Oklahoma'),
    ('OR', 'Oregon'),('PA', 'Pennsylvania'),('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),('SC', 'South Carolina'),('SD', 'South Dakota'),
    ('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),
    ('VT', 'Vermont'),('VA', 'Virginia'),('VI', 'Virgin Islands'),
    ('WA', 'Washington'),('WV', 'West Virginia'),('WI', 'Wisconsin'),('WY', 'Wyoming')
)

CATAGORIES = (
    ('AG', 'Aging'),('AF', 'Agriculture and Food'),('AC', 'Arts and Culture'),
    ('AS', 'Athletics and Sports'),('CY', 'Children and Youth'),('AF', 'After School'), ('CS', 'Civil Society'),
    ('CE', 'Community and Economic Development'),('CT', 'Computers and Technology'),('CP', 'Consumer Protection'),
    ('CR', 'Crime and Safety'),('DI', 'Disabilities'),('DO', 'Domestic Violence Prevention'),
    ('EL', 'Education and Literacy'), ('K2', 'K 12'), ('HE', 'Higher Education'), ('CR', 'Career Preparation'), ('AE', 'Adult Education'),('EM', 'Employment and Labor'),('EE', 'Energy and Environment'),
    ('LI', 'LGBTQ+'),('GR', 'Government Reform'),('HW', 'Health and Wellness'),
    ('HO', 'Housing and Homelessness'),('HR', 'Human Rights and Civil Liberties'),('HU', 'Hunger'),
    ('IM', 'Immigration'),('JM', 'Journalism and Media'),('MB', 'Men and Boys'),
    ('NP', 'Nonprofit Empowerment'),('PF', 'Parenting and Families'),('PO', 'Poverty'),
    ('PJ', 'Prison and Judicial Reform'),('RE', 'Race and Ethnicity'),('RI', 'Religion'),
    ('SC', 'Science, Technology, Engineering and Math'),('SA', 'Substance Abuse and Recovery'),('TR', 'Transportation'),
    ('WE', 'Welfare and Public Assistance'),('WG', 'Woman and Girls')
)

class Organization(models.Model):
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    contact_title = models.CharField(max_length=200)
    contact_email = models.EmailField(_('email address'))
    address = models.CharField(max_length=200)
    city =  models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATES)
    zip_code = models.CharField(max_length=10)
    phone = PhoneField(blank=True, help_text='Org. Contact Phone')
    website_url = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=CATAGORIES)
    ein = models.CharField(max_length=15)
    fiscal_sponsor = models.CharField(max_length = 200, default='', blank=True)
    guidestar_url = models.CharField(max_length = 200, default='', blank=True)
    logo_url = models.CharField(max_length = 200, default='https://www.resetyourbody.com/wp-content/uploads/COMPANY_LOGO/logo-default.png', blank='True')
    #video_url TODO ICE BOX

    description = models.TextField(max_length=500, verbose_name='about us')
    mission_statement = models.TextField(max_length=500, verbose_name='mission statement')
    verified = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('org_details', kwargs={'pk': self.id})
    
    def get_donations(self):
        return self.donation_set.all().order_by('-id')[:8]

# class SocialMedia(model.Model):
#     facebook_url = models.CharField(max_length=200)
#     twitter_url = models.CharField(max_length=200)
#     instagram_url = models.CharField(max_length=200)
    
class BoardMember(models.Model):
    member = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.member

class Review(models.Model):
    content = models.TextField(max_length=256)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.id}) {self.organization} {self.user}'

class Gallery(models.Model):
    picture_url = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.organization} picture id ({self.id})'

class Donation(models.Model):
    amount = models.FloatField(default=50.00)
    anonymous = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} org ({self.organization.id}) amount ${self.amount}'