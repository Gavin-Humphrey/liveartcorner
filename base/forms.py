from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MaxLengthValidator,
)

from user.models import User, ArtistProfile, ArtistAvailability
from item.models import CardItems, Item
from services.models import Service, Booking


# class RegisterForm(UserCreationForm):
#     is_artist = forms.BooleanField(required=False, initial=False, label='Register as an artist')
#     class Meta:
#         model = User
#         fields = ["name", "email", "password1", "password2"]


class RegisterForm(UserCreationForm):
    is_artist = forms.BooleanField(
        required=False, initial=False, label="Register as an artist"
    )
    phone_number = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                r"^\+\d{1,2}\s?[\d\-()]+\s?[\d\-()]+$",
                message="Invalid phone number format.",
            )
        ],
    )
    street_address = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                r"^[A-Za-z0-9\s\,\.]+$", message="Invalid characters in street address."
            ),
        ],
    )
    city = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(50),  # Example maximum length
        ],
    )
    postal_code = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\d{5}-\d{4}|\d{5}$",
                message="Invalid postal code format. Please use XXXXX or XXXXX-XXXX format.",
            )
        ],
    )
    country = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(50),  # Example maximum length
        ],
    )

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "phone_number",
            "street_address",
            "city",
            "postal_code",
            "country",
            "password1",
            "password2",
        )

    # Additional validations if needed
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


# import re

# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     phone_number = forms.CharField(max_length=15, required=True)
#     street_number = forms.CharField(max_length=10, required=True)
#     street_name = forms.CharField(max_length=255, required=True)
#     city = forms.CharField(max_length=100, required=True)
#     area_code = forms.CharField(max_length=10, required=True)
#     country = forms.CharField(max_length=100, required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'phone_number', 'street_number', 'street_name', 'city', 'area_code', 'country', 'password1', 'password2']

#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number')
#         if not re.match(r'^\+?1?\d{9,15}$', phone_number):
#             raise forms.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#         return phone_number

#     def clean_area_code(self):
#         area_code = self.cleaned_data.get('area_code')
#         if not re.match(r'^\d{5}$', area_code):
#             raise forms.ValidationError("Area code must be exactly 5 digits.")
#         return area_code

#     def clean_street_name(self):
#         street_name = self.cleaned_data.get('street_name')
#         if not re.match(r'^[A-Za-z0-9\s,.-]+$', street_name):
#             raise forms.ValidationError("Street name contains invalid characters.")
#         return street_name

#     def clean_city(self):
#         city = self.cleaned_data.get('city')
#         if not re.match(r'^[A-Za-z\s]+$', city):
#             raise forms.ValidationError("City contains invalid characters.")
#         return city

#     def clean_country(self):
#         country = self.cleaned_data.get('country')
#         if not re.match(r'^[A-Za-z\s]+$', country):
#             raise forms.ValidationError("Country contains invalid characters.")
#         return country

#     def clean_street_number(self):
#         street_number = self.cleaned_data.get('street_number')
#         if not re.match(r'^[0-9]+$', street_number):
#             raise forms.ValidationError("Street number contains invalid characters.")
#         return street_number

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.phone_number = self.cleaned_data['phone_number']
#         user.street_number = self.cleaned_data['street_number']
#         user.street_name = self.cleaned_data['street_name']
#         user.city = self.cleaned_data['city']
#         user.area_code = self.cleaned_data['area_code']
#         user.country = self.cleaned_data['country']
#         if commit:
#             user.save()
#         return user


class UserProfileForm(ModelForm):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["name", "email"]


class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = [
            "bio",
            "profile_picture",
            #'portfolio_url',
            "phone_number",
            "location",
            "artistic_medium",
            "experience_education",
        ]


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "name", "is_artist", "is_vetted_artist", "avatar"]


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "length",
            "width",
            "price",
            "quantity",
            "image",
        ]

        widgets = {"image": forms.FileInput(attrs={"enctype": "multipart/form-data"})}


class DeliveryInfoForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full Name", required=False)
    address = forms.CharField(
        label="Address", required=False
    )  # , widget=forms.Textarea)
    email = forms.EmailField(label="Email", required=False)
    phone_number = forms.CharField(label="Phone Number", required=False, max_length=20)


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
        exclude = ["artist"]
        fields = ["name", "description", "duration", "price"]


class ArtistAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ArtistAvailability
        fields = ["date", "start_time", "end_time"]  # Use fields from the model
        widgets = {
            "start_datetime": forms.SplitDateTimeWidget(),  # Adjust widgets accordingly
            "end_datetime": forms.SplitDateTimeWidget(),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []
