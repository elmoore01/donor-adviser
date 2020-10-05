from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q

from .forms import OrganizationForm, DonationForm, BoardMemberForm
from .models import Organization, Review, Gallery, BoardMember

# Create your views here.
def home_page(request):
    featured = Organization.objects.all().order_by('-id')[:3]
    return render(request, 'main_app/home.html', {
        'featured': featured
    })

def contact_page(request):
    return render(request, 'main_app/contact.html')

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'main_app/organizations/details.html'


class OrganizationResultsView(ListView):
    model = Organization
    template_name = 'main_app/organizations/results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        location = self.request.GET.get('l')
        category = self.request.GET.get('c')
        if not query and not location and not category:
            return Organization.objects.order_by('-name').all()
        if not query:
            query = 'None'
        if not location:
            location = 'None'            
        if not category:
            category = 'None'
        return Organization.objects.filter(
            Q(name__icontains=query) |
            Q(ein__icontains=query) |
            Q(address__icontains=location) |
            Q(city__icontains=location) |
            Q(state__icontains=location) |
            Q(zip_code=location) |
            Q(category__icontains=category)
        )

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'main_app/organizations/update.html'
    fields = [
            'name', 'fiscal_sponsor', 'ein', 'contact_name', 'contact_title', 'contact_email', 'address', 'city', 
            'state', 'zip_code', 'phone', 'website_url', 'category', 'guidestar_url', 'logo_url', 'mission_statement', 'description',
    ]

@login_required
def organization_delete(request, pk):
    org = Organization.objects.get(id=pk)
    if not org:
        return redirect('org_details', pk=pk)
    if org.user == request.user:
        org.delete()
    return redirect('org_results')

@login_required
def organization_create(request):
    if not request.user.is_partial_complete():
        return redirect('account_update')
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            new_org = form.save(commit=False)
            new_org.user_id = request.user.id
            new_org.save()
            return redirect('org_details', pk=new_org.id)
        return redirect('org_results')
    org_form = OrganizationForm()
    return render(request, 'main_app/organizations/create.html', {
        'org_form': org_form
    })

@login_required
def org_gallery_create(request, pk):
    org = Organization.objects.get(id=pk)
    if request.user == org.user:
        photo_url = request.POST.get('photo_url')
        Gallery.objects.create(picture_url=photo_url, organization_id=pk)
    return redirect('org_details', pk=pk)

@login_required
def org_gallery_delete(request, pk, photo_id):
    org = Organization.objects.get(id=pk)
    if request.user == org.user:
        Gallery.objects.get(id=photo_id).delete()
    return redirect('org_details', pk=pk)


@login_required
def org_review_create(request, pk):
    content = request.POST.get('content')
    Review.objects.create(content=content, user_id=request.user.id, organization_id=pk)
    return redirect('org_details', pk=pk)
    
@login_required
def org_review_delete(request, pk, review_id):
    review = Review.objects.get(id=review_id)
    if not review:
        return redirect('org_details', pk=pk)
    if review.user == request.user:
        review.delete()
    return redirect('org_details', pk=pk)

@login_required
def org_donate_create(request, pk):
    if not request.user.is_partial_complete():
        return redirect('account_update')
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            new_donation = form.save(commit=False)
            new_donation.user_id = request.user.id
            new_donation.organization_id = pk
            new_donation.amount = request.POST.get('total_amount')
            new_donation.save()
        return redirect('org_details', pk=pk)
    org = Organization.objects.get(id=pk)
    donate_form = DonationForm()
    return render(request, 'main_app/organizations/donations/create.html', {
        'donate_form': donate_form,
        'org': org
    })

@login_required
def org_members_view(request, pk):
    org = Organization.objects.get(id=pk)
    if request.user != org.user:
        return redirect('org_details', pk=pk)
    member_form = BoardMemberForm()
    return render(request, 'main_app/organizations/members/details.html', {
        'org':org,
        'member_form': member_form
    })

@login_required
def org_members_create(request, pk):
    org = Organization.objects.get(id=pk)
    if request.user != org.user:
        return redirect('org_details', pk=pk)
    form = BoardMemberForm(request.POST)
    if form.is_valid():
        new_member = form.save(commit=False)
        new_member.organization_id = pk
        new_member.save()
    return redirect('org_members_view', pk=pk)

@login_required
def org_members_delete(request, pk, member_id):
    org = Organization.objects.get(id=pk)
    if request.user != org.user:
        return redirect('org_details', pk=pk)
    BoardMember.objects.get(id=member_id).delete()
    return redirect('org_members_view', pk=pk)
