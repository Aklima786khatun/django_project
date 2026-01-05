from django.contrib import admin
from .models import Donor, Volunteer, Donation, Gallery, DonationArea
from .models import Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')





@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    # Ensure 'user', 'contact', 'address', and 'regdate' exist in your Donor model
    list_display = ('id', 'user', 'contact', 'address', 'regdate')
    
@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'address', 'status', 'regdate')
    
@admin.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    # Note: verify if the field is 'areaname' or just 'name' in your models.py
    list_display = ('id', 'areaname', 'description', 'creationdate')
    
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    # Removed 'volunteer' and 'donationarea' because they caused the E108 error
    list_display = ('id', 'donor', 'donationname')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    # Removed 'volunteer' and 'donationarea' because they caused the E108 error
    list_display = ('id', 'donation')