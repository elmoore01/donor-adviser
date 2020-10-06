from django.contrib import admin
from .models import Organization, Review, BoardMember, Gallery, Donation

# Register your models here.
admin.site.register(Organization)
admin.site.register(Review)
admin.site.register(BoardMember)
admin.site.register(Gallery)
admin.site.register(Donation)
