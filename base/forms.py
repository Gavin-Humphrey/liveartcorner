from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import  User, ArtistProfile, ArtistAvailability
from item.models import CardItems, Item
from services.models import Service, Booking



class RegisterForm(UserCreationForm):
    is_artist = forms.BooleanField(required=False, initial=False, label='Register as an artist')
    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]


class UserProfileForm(ModelForm):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = [ "name", "email"] 


class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = [
            'bio',
            'profile_picture',
            #'portfolio_url',
            'phone_number',
            'location',
            'artistic_medium',
            'experience_education'
        ]

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'is_artist', 'is_vetted_artist', 'avatar'] 


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "length", "width", "price", "quantity", "image" ]

        widgets = {
            'image': forms.FileInput(attrs={'enctype': 'multipart/form-data'})
        }
 

class DeliveryInfoForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name', required=False)
    address = forms.CharField(label='Address', required=False)#, widget=forms.Textarea)
    email = forms.EmailField(label='Email', required=False)
    phone_number = forms.CharField(label='Phone Number', required=False, max_length=20)


class PaymentForm(forms.Form):
    stripe_token = forms.CharField(widget=forms.HiddenInput())
  
class ContactForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)




# Services
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['artist']
        fields = ['name', 'description', 'duration', 'price']



class ArtistAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ArtistAvailability
        fields = ['date', 'start_time', 'end_time']  # Use fields from the model
        widgets = {
            'start_datetime': forms.SplitDateTimeWidget(),  # Adjust widgets accordingly
            'end_datetime': forms.SplitDateTimeWidget(),
        }

        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  

