from django import forms
from django.contrib.auth.models import User
from .models import Donor,Volunteer,Donation,DonationArea
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import password_validation


class LoginForm(AuthenticationForm):
    username =UsernameField(required=True,widget=forms.TextInput(attrs={'autofocus ':'True', 'class':'form-control','placeholder':'username'}))
    password =forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password Again'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),}

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['address', 'contact']  
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'})}

class DonorSignupForm(forms.ModelForm):
    userpic = forms.ImageField(widget=forms.TextInput(attrs={'class':'form-control'})),
    class Meta:
        model = Donor
        fields = ['contact','userpic','address']  
        widgets = {
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'})}
        
class VolunteerSignupForm(forms.ModelForm):    
    userpic = forms.ImageField(label="User Picture")
    idpic = forms.ImageField(label="ID Proof Picture")
    class Meta:
        model = Volunteer
        fields = ['contact', 'userpic', 'idpic', 'address', 'aboutme']
        widgets = {
            'contact': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
            'aboutme': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'About Me'}),
            'userpic': forms.FileInput(attrs={'class': 'form-control'}),
            'idpic': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control','placeholder':'Old Password'}))
    new_password1 = forms.CharField(label="New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control','placeholder':'New Password'}),
    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=" onfirm New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control','placeholder':'Confirm Password'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email",max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control','placeholder':'New Password'}),
    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=" onfirm New Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control','placeholder':'Confirm Password'}))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donationname', 'donationpic', 'collectionloc', 'description']
        widgets = {
            'donationname': forms.TextInput(attrs={'class': 'form-control'}),
            'collectionloc': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DonationNewForm(forms.ModelForm):
    donationpic = forms.ImageField(),
    class Meta:
        model = Donation
        fields = ['donationname', 'donationpic', 'collectionloc', 'description']
        widgets = {
            'donationname': forms.TextInput(attrs={'class': 'form-control'}),
            'collectionloc': forms.TextInput(attrs={'class': 'form-control','placeholder':'Donation Collection Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Description(Special Note)'}),
            'donationpic': forms.FileInput(attrs={'class':'form-control'}),
        }
        labels={
            'donationname': "Donation Image(Pic of Item you want to donate)",
            'collectionloc': "Donation Name",
            'description': "Donation Collection Address",
            'donationpic': "Description (Special Note)",
        }

class DonationAreaForm(forms.ModelForm):
    class Meta:
        model = DonationArea
        fields = ['areaname','description']
        widgets = {
            'areaname': forms.TextInput(attrs={'class': 'form-control','placeholder':'Donation Area'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder':'Description'}),
        }
        labels={
            'areaname':"Donation Area Name",
            'description':"Description",
        }


