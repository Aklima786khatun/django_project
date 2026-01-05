from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Slider, Donor, Volunteer, Donation, DonationArea,Gallery
from .forms import (
    UserForm, DonorSignupForm, VolunteerSignupForm, 
    LoginForm, MyPasswordChangeForm,DonationNewForm,DonationAreaForm
)
from .forms import LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import MyPasswordChangeForm
from datetime import date


def index(request):
    # Fetch only the active sliders, ordered by your 'Order' field
    slider_data = Slider.objects.filter(is_active=True).order_by('order') 
    return render(request, 'index.html', {'carousels': slider_data})

def index(request):
    return render(request, "index.html")

def gallery(request):
    gallery = Gallery.objects.all()
    return render(request, "gallery.html",locals())

def about_view(request):
    return render(request, 'about.html')

# --- LOGIN VIEWS ---

class login_admin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-admin.html",locals())

    def post(self, request):
        us = request.POST.get('username')
        pwd = request.POST.get('password')
        try:
            user = authenticate(username=us, password=pwd)
            if user:
                if user.is_staff:
                    login(request, user)
                    return redirect('index_admin')
                else:
                    messages.warning(request, 'Invalid Admin Credentials')
            else:
                messages.warning(request, 'Invalid username and password')
        except:
            messages.warning(request, 'Login Failed')
        return render(request, "login-admin.html",locals())

class login_donor(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-donor.html", {'form': form})

    def post(self, request):
        us = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(username=us, password=pwd)
        if user and Donor.objects.filter(user=user).exists():
            login(request, user)
            messages.success(request, 'Login Successfully')
            return redirect('index_donor')
        messages.warning(request, 'Invalid Donor Credentials')
        return render(request, "login-donor.html")

class login_volunteer(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-volunteer.html", {'form': form})

    def post(self, request):
        us = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(username=us, password=pwd)
        if user and Volunteer.objects.filter(user=user).exists():
            login(request, user)
            messages.success(request, 'Login Successfully')
            return redirect('index_volunteer')
        messages.warning(request, 'Invalid Volunteer Credentials')
        return render(request, "login-volunteer.html")

# --- SIGNUP VIEWS ---

class signup_donor(View):
    def get(self, request):
        form1 = UserForm()
        form2 = DonorSignupForm()
        return render(request, "signup_donor.html", locals())

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = DonorSignupForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            try:
                user = User.objects.create_user(
                    first_name=form1.cleaned_data['first_name'],
                    last_name=form1.cleaned_data['last_name'],
                    username=form1.cleaned_data['username'],
                    email=form1.cleaned_data['email'],
                    password=form1.cleaned_data['password1']
                )
                Donor.objects.create(
                    user=user, 
                    contact=form2.cleaned_data['contact'], 
                    userpic=request.FILES.get('userpic'),
                    address=form2.cleaned_data['address']
                )
                messages.success(request, 'Donor Profile Created Successfully!')
                return redirect('login_donor')
            except Exception as e:
                messages.warning(request, 'Error: Username already exists.')
        return render(request, "signup_donor.html", locals())

class signup_volunteer(View):
    def get(self, request):
        form1 = UserForm()
        form2 = VolunteerSignupForm()
        return render(request, "signup_volunteer.html", locals())

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = VolunteerSignupForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            try:
                user = User.objects.create_user(
                    first_name=form1.cleaned_data['first_name'],
                    last_name=form1.cleaned_data['last_name'],
                    username=form1.cleaned_data['username'],
                    email=form1.cleaned_data['email'],
                    password=form1.cleaned_data['password1']
                )
                Volunteer.objects.create(
                    user=user, 
                    contact=form2.cleaned_data['contact'], 
                    userpic=request.FILES.get('userpic'),
                    idpic=request.FILES.get('idpic'),
                    address=form2.cleaned_data['address'],
                    aboutme=form2.cleaned_data['aboutme'],
                    status='pending'
                )
                messages.success(request, 'Volunteer Profile Created Successfully!')
                return redirect('login_volunteer')
            except Exception as e:
                messages.warning(request, 'Error: Username already exists.')
        return render(request, "signup_volunteer.html", locals())

# --- ADMIN VIEWS ---

def index_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    totaldonations = Donation.objects.all().count()
    totaldonors = Donor.objects.all().count()
    totalvolunteers = Volunteer.objects.all().count()
    totalpendingdonations = Donation.objects.filter(status="pending").count()
    totalaccepteddonations = Donation.objects.filter(status="accept").count()
    totaldelivereddonations = Donation.objects.filter(status="Donation Delivered Successfully").count()
    totaldonationareas = DonationArea.objects.all().count()
    return render(request, "index-admin.html",locals())

def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='pending')
    return render(request, "pending-donation.html",locals())

def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='accept')
    return render(request, "accepted-donation.html",locals())

def rejected_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='reject')
    return render(request, "rejected-donation.html",locals())

def volunteerallocated_donation(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Volunteer Allocated')
    return render(request, "volunteerallocated-donation.html",locals())

def donationrec_admin(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Donation Received')
    return render(request, "donationrec-admin.html",locals())

def donationnotrec_admin(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Donation Not Received')
    return render(request, "donationnotrec-admin.html",locals())

def donationdelivered_admin(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Donation Delivered Successfully')
    
    return render(request, "donationdelivered-admin.html",locals())

def all_donations(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.all()
    return render(request, "all-donations.html",locals())

def delete_donation(request,pid): 
    donation = Donation.objects.get(id=pid)
    donation.delete()
    return redirect('all_donations')
    
def manage_donor(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donor = Donor.objects.all()
    return render(request, "manage-donor.html",locals())

def new_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status='pending')
    return render(request, "new-volunteer.html",locals())

def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status='accept')
    return render(request, 'accepted_volunteer.html',locals())

def rejected_volunteer(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status='reject')
    return render(request, "rejected-volunteer.html",locals)

def all_volunteer(request): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.all()
    return render(request, "all-volunteer.html",locals())

def delete_volunteer(request,pid): 
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all_volunteer')

def add_area(View): 
    def get(self,request):
        form = DonationAreaForm()
        return render(request, "add-area.html",locals())
    def post(self,request):
        form = DonationAreaForm(request,post)
        if not request.is_authenticated:
            return redirect('/login-admin')
        areaname = request.POST['areaname']
        des = request.POST['description']
        try:
            DonationArea.objects.create(areaname=areaname,description=des)
            messages.success(request,'Area Added Successfully')
        except:
            messages.warning(request,'Area Not Added')
        return render(request,"Add-area.html",locals())
    
class edit_area(View): 
    def get(self,request,pid):
        form = DonationAreaForm()
        area = DonationArea.objects.get(id=pid)
        return render(request, "edit-area.html",locals())
    def post(self,request,pid):
        if not request.is_authenticated:
            return redirect('/login-admin')
        form = DonationAreaForm(request,post)
        areaname = request.POST['areaname']
        description = request.POST['description']
        area.areaname = areaname
        area.description = description
        try:
            area.save()
            messages.success(request,'Area Updated Successfully')
            return redirect('manage_area')
        except:
            messages.warning(request,'Area Not Updated')
        return render(request, "edit-area.html",locals)

def manage_area(request): 
    if not request.is_authenticated:
        return redirect('/login-admin')
    area = DonationArea.objects.all()
    return render(request, "manage-area.html",locals())
    
def delete_area(request,pid): 
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    area = DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('manage_area')

class changepwd_admin(View):
    def get(self, request):
        form = MyPasswordChangeForm(user=request.user)
        return render(request, "changepwd-admin.html", locals())

    def post(self, request):
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Updated Successfully')
            return redirect('index_admin')
        return render(request, "changepwd-admin.html", locals())

def logoutView(request):
    logout(request)
    return redirect("index")

# --- DETAIL VIEWS ---
class accepted_donationdetail(View):
    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('login_admin')
        
        # 1. Fetch the donation
        donation = Donation.objects.get(id=pid)
        
        # 2. Update the status
        donation.status = "accepted"
        donation.save()
        
        # 3. Success Message and Redirect
        messages.success(request, "Donation request accepted successfully!")
        return redirect('accepted_donation') # Redirect to the 'Accepted Donations' list

class view_volunteerdetail(View):
    def get(self,request, pid):
        if not request.user.is_authenticated:
            return redirect('login_admin')
        volunteer = Volunteer.objects.get(id=pid)
        return render(request, "view-donationdetail.html", locals())
    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('login_admin')
        volunteer = Volunteer.objects.get(id=pid)
        status = request.POST['status']
        adminremark = request.POST('adminremark')
        try:
            volunteer.adminremark = adminremark
            volunteer.status = status
            volunteer.updationdate = date.today()
            volunteer.save()
            messages.success(request,'Volunteer Updated successfully')   
        except Exception as e:
            messages.error(request, f"Error updating donation: {e}")
        return render(request, "view-volunteerdetail.html",locals())

def view_donordetail(request, pid):
    if not request.user.is_authenticated:
            return redirect('login_admin')
    donor = Donor.objects.get(id=pid)
    return render(request, "view-donordetail.html",locals())

def view_donationdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    
    donation = Donation.objects.get(id=pid)
    
    if request.method == "POST":
        status = request.POST.get('status')
        remark = request.POST.get('adminremark')
        
        donation.status = status
        donation.adminremark = remark
        donation.updationdate = date.today()
        donation.save()
        
        messages.success(request, f"Donation status updated to {status}")
        return redirect('all_donations')
        
    return render(request, 'view-donationdetail.html', {'donation': donation})

def index_donor(request):
    if not request.user.is_authenticated:
            return redirect('login-donor')
    user = request.user
    donor = Donor.objects.get(user=user)
    donationaccount = Donation.objects.filter(donor=donor).count()
    acceptedaccount = Donation.objects.filter(donor=donor,status="accept").count()
    rejectedaccount = Donation.objects.filter(donor=donor,status="reject").count()
    pendingaccount = Donation.objects.filter(donor=donor,status="pending").count()
    deliveredaccount = Donation.objects.filter(donor=donor,status="Donation Delivered Successfully").count()
    return render(request, "index-donor.html",locals())

class donate_now(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login_donor')
        return render(request, 'donate-now.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login_donor')
        
        # Pull data using the 'name' attributes from your HTML
        d_name = request.POST.get('donationname')
        d_pic = request.FILES.get('donationpic')
        d_loc = request.POST.get('collectionloc')
        d_desc = request.POST.get('description')
        
        try:
            donor = Donor.objects.get(user=request.user)
            Donation.objects.create(
                donor=donor,
                donationname=d_name,
                donationpic=d_pic,
                collectionloc=d_loc,
                description=d_desc,
                status="pending",
                donationdate=date.today()
            )
            messages.success(request, 'Donation submitted successfully!')
            return redirect('donation_history')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, "donate-now.html")

def donation_history(request):
    if not request.user.is_authenticated:
        return redirect('login_donor')
    
    # Get the donor object linked to the logged-in user
    donor = Donor.objects.get(user=request.user)
    
    # Filter donations specifically for this donor
    donation = Donation.objects.filter(donor=donor).order_by('-donationdate')
    
    return render(request, 'donation-history.html', {'donation': donation})

def profile_donor(request): 
    if not request.user.is_authenticated:
            return redirect('login-donor')
    user = request.user
    donor = Donor.objects.get(user=user)
    donationaccount = Donation.objects.filter(donor=donor).count()
    acceptedaccount = Donation.objects.filter(donor=donor,status="accept").count()
    rejectedaccount = Donation.objects.filter(donor=donor,status="reject").count()
    pendingaccount = Donation.objects.filter(donor=donor,status="pending").count()
    deliveredaccount = Donation.objects.filter(donor=donor,status="Donation Delivered Successfully").count()
    return render(request, "profile-donor.html")

class changepwd_donor(View):
    def get(self, request):
        form = MyPasswordChangeForm(user=request.user)
        return render(request, "changepwd-donor.html", locals())

    def post(self, request):
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed')
            return redirect('index_donor')
        return render(request, "changepwd-donor.html", locals())

# --- VOLUNTEER VIEWS ---

def index_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('login_volunteer')
    
    # Fetch the Volunteer object associated with the logged-in user
    volunteer = get_object_or_404(Volunteer, user=request.user)
    
    # Stats for the Volunteer Dashboard
    total_assigned = Donation.objects.filter(Volunteer=volunteer).count()
    pending_collections = Donation.objects.filter(Volunteer=volunteer, status='Volunteer Allocated').count()
    received_donations = Donation.objects.filter(Volunteer=volunteer, status='Donation Received').count()
    delivered_donations = Donation.objects.filter(Volunteer=volunteer, status='Donation Delivered Successfully').count()
    
    return render(request, "index-volunteer.html", locals())

def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('login_volunteer')
    
    volunteer = get_object_or_404(Volunteer, user=request.user)
    # Get donations assigned to this volunteer that are ready for collection
    donation = Donation.objects.filter(volunteer=volunteer, status='Volunteer Allocated')
    
    return render(request, "collection-req.html", locals())

def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('login_volunteer')
    
    volunteer = get_object_or_404(Volunteer, user=request.user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Received')
    
    return render(request, "donationrec-volunteer.html", locals())

def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('login_volunteer')
    
    volunteer = get_object_or_404(Volunteer, user=request.user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Not Received')
    
    return render(request, "donationnotrec-volunteer.html", locals())

def donationdelivered_volunteer(request): 
    if not request.user.is_authenticated:
        return redirect('login_volunteer')
    
    volunteer = get_object_or_404(Volunteer, user=request.user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Delivered Successfully')
    
    return render(request, "donationdelivered-volunteer.html", locals())

def profile_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('login_volunteer')
    
    volunteer = get_object_or_404(Volunteer, user=request.user)
    return render(request, "profile-volunteer.html", locals())
class changepwd_volunteer(View):
    def get(self, request):
        form = MyPasswordChangeForm(user=request.user)
        # Change hyphen (-) to underscore (_)
        return render(request, "changepwd-volunteer.html", locals())

    def post(self, request):
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed Successfully!')
            return redirect('index_volunteer')
        # Change hyphen (-) to underscore (_)
        return render(request, "changepwd-volunteer.html", locals())

# --- DONOR DETAIL VIEWS ---

def donationdetail_donor(request, pid): 
    if not request.user.is_authenticated:
        return redirect('login_donor')
    
    # 1. Fetch the specific donation using the ID (pid)
    donation = get_object_or_404(Donation, id=pid)
    
    # 2. Sidebar/Stats logic
    donor = Donor.objects.get(user=request.user)
    donationaccount = Donation.objects.filter(donor=donor).count()
    acceptedaccount = Donation.objects.filter(donor=donor, status="accept").count()
    rejectedaccount = Donation.objects.filter(donor=donor, status="reject").count()
    pendingaccount = Donation.objects.filter(donor=donor, status="pending").count()
    deliveredaccount = Donation.objects.filter(donor=donor, status="Donation Delivered Successfully").count()
    
    # 3. Return the CORRECT template
    return render(request, "donationdetail-donor.html", locals())

def donationcollection_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_donor')
    
    donation = get_object_or_404(Donation, id=pid)
    return render(request, "donationcollection-detail.html", locals())

def donationrec_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_donor')
    
    donation = get_object_or_404(Donation, id=pid)
    return render(request, "donationrec-detail.html", locals())

# --- VOLUNTEER DETAIL VIEW (Fixed) ---

class view_volunteerdetail(View):
    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('login_admin')
        # Corrected variable name: using 'volunteer' instead of 'donation'
        volunteer = get_object_or_404(Volunteer, id=pid)
        return render(request, "view-volunteerdetail.html", locals())

    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('login_admin')
        
        volunteer = get_object_or_404(Volunteer, id=pid)
        status = request.POST.get('status')
        adminremark = request.POST.get('adminremark')
        
        try:
            volunteer.adminremark = adminremark
            volunteer.status = status
            volunteer.updationdate = date.today()
            volunteer.save()
            messages.success(request, 'Volunteer status updated successfully')
            return redirect('all_volunteer') 
        except Exception as e:
            messages.error(request, f"Error updating volunteer: {e}")
            return render(request, "view-volunteerdetail.html", locals())