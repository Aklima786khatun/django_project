from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=100, blank=True)
    # Change 'upload_url' to 'upload_to'
    image = models.ImageField(upload_to='sliders/') 
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self): # Also fixed the typo here (was __cl__)
        return self.title if self.title else f"Slider {self.id}"

    class Meta:
        ordering = ['order']
class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15,null=True)
    address = models.TextField(max_length=500,null=True)
    userpic = models.ImageField(upload_to='donor/', null=True, blank=True)
    regdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15,null=True)
    address = models.TextField(max_length=500,null=True)
    userpic = models.ImageField(upload_to='volunteer/', null=True, blank=True)
    idpic = models.ImageField(upload_to='volunteer/', null=True, blank=True)
    aboutme = models.TextField(max_length=1000, null=True)
    status = models.CharField(max_length=20, default='pending')
    regdate = models.DateTimeField(auto_now_add=True)
    adminremarks = models.TextField(max_length=500, null=True)
    updationdate = models.DateTimeField(null=True)
    def __str__(self):
        return self.user.username
class DonationArea(models.Model):
    areaname = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creationdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.areaname
class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donationname = models.CharField(max_length=200,null=True)
    donationpic = models.ImageField(upload_to='donation/', null=True, blank=True)
    collectionloc = models.CharField(max_length=300,null=True)
    description = models.TextField(max_length=1000,null=True)
    status = models.CharField(max_length=20, default='pending')
    donationitem = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100)
    donationpic = models.ImageField(upload_to='donation/', null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    donationdate = models.DateField(null=True)
    adminremarks = models.TextField(max_length=500, null=True)
    Volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    donationarea = models.ForeignKey(DonationArea, on_delete=models.CASCADE, null=True)
    volunteerremark = models.TextField(max_length=500, null=True)
    updationdate = models.DateTimeField(null=True)
    def __str__(self):
        return self.id
class Gallery(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    deliverypic = models.FileField(null=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id
    