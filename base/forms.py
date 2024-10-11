from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MaxLengthValidator,
)

from user.models import User, ArtistProfile, ArtistAvailability
from item.models import Item
from services.models import Service, Booking

import re


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
        required=True,
        validators=[
            RegexValidator(
                r"^\+?\d{0,15}$",
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
            MaxLengthValidator(50),
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
            MaxLengthValidator(50),
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

    # Additional validations
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


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
    current_image = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"}), required=False
    )

    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "length",
            "width",
            "price",
            "quantity",
            "current_image",
            "image",
        ]
        widgets = {
            "image": forms.FileInput(attrs={"enctype": "multipart/form-data"}),
            "current_image": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["current_image"].initial = (
                self.instance.image.url if self.instance.image else ""
            )
            self.fields["image"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance and self.instance.pk:
            if not self.cleaned_data.get("image") and self.instance.image:
                instance.image = self.instance.image
        if commit:
            instance.save()
        return instance


# email validator
def validate_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None


class DeliveryInfoForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="full_name", required=True)
    email = forms.EmailField(label="email", required=True)
    address = forms.CharField(max_length=255, label="address", required=True)
    city = forms.CharField(max_length=100, label="city", required=True)
    postcode = forms.CharField(max_length=10, label="postcode", required=True)
    country = forms.CharField(max_length=50, label="country", required=True)
    phone_number = forms.CharField(label="phone_number", required=True, max_length=20)

    # Custom Validation for full name
    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if not full_name:
            raise forms.ValidationError("full_name is required.")
        if not re.match(r"^[A-Za-z\s-]+$", full_name):
            raise forms.ValidationError(
                "Full name should contain only letters, spaces, and hyphens."
            )
        return full_name

    # Custom Validation for email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not validate_email(email):
            raise forms.ValidationError(
                "Invalid email format. Please enter a valid email address."
            )
        return email

    # Custom Validation for city
    def clean_city(self):
        city = self.cleaned_data.get("city")
        if not city:
            raise forms.ValidationError("City is required.")
        if not re.match(r"^[A-Za-z\s-]+$", city):
            raise forms.ValidationError(
                "City should contain only letters, spaces, and hyphens."
            )
        return city

    # Custom Validation for postcode (must be numeric)
    def clean_postcode(self):
        postcode = self.cleaned_data.get("postcode")
        if not postcode.isdigit():
            raise forms.ValidationError("Postcode must be numeric.")
        return postcode

    # Custom Validation for country
    def clean_country(self):
        country = self.cleaned_data.get("country")
        if not country:
            raise forms.ValidationError("Country is required.")
        # Updated regex to allow multiple words with spaces
        if not re.match(r"^[A-Za-z]+(?:\s[A-Za-z]+)?(?:\s[A-Za-z]+)?$", country):
            raise forms.ValidationError(
                "Country should contain only letters and spaces."
            )
        return country

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not re.match(r"^\+\d{1,3}\s?\d{1,15}$", phone_number):
            raise forms.ValidationError(
                "Phone number must contain country code and only digits."
            )
        return phone_number


class PaymentForm(forms.Form):
    stripe_token = forms.CharField(widget=forms.HiddenInput())


# Services
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ["artist"]
        fields = ["name", "description", "duration", "price"]


class ArtistAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ArtistAvailability
        fields = ["date", "start_time", "end_time"]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "placeholder": "YYYY-MM-DD"}
            ),
            "start_time": forms.TimeInput(
                attrs={"type": "time", "placeholder": "HH:MM"}
            ),
            "end_time": forms.TimeInput(attrs={"type": "time", "placeholder": "HH:MM"}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []
