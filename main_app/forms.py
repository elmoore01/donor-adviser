from django.forms import ModelForm

from .models import Organization, Donation, BoardMember

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        labels = {
            'description': 'About Us',
            'mission_statement': 'Mission Statement'
        }
        fields = [
            'name', 'ein', 'address', 'city', 
            'state', 'zip_code', 'phone','contact_email','website_url', 'category',
            'fiscal_sponsor','guidestar_url', 'logo_url', 'mission_statement', 'description',
        ]

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        labels = {
            'amount': 'Donation amount',
            'anonymous': 'Remain Anonymous?'
        }
        fields = ['amount', 'anonymous']

class BoardMemberForm(ModelForm):
    class Meta:
        model = BoardMember
        labels = {
            'member': 'Full Name',
        }
        fields = ['member','email', 'company', 'title']