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
    current_image = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)

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
            "image"
        ]
        widgets = {
            "image": forms.FileInput(attrs={"enctype": "multipart/form-data"}),
            "current_image": forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['current_image'].initial = self.instance.image.url if self.instance.image else ""
            self.fields['image'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance and self.instance.pk:
            if not self.cleaned_data.get('image') and self.instance.image:
                instance.image = self.instance.image
        if commit:
            instance.save()
        return instance


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
        fields = ["date", "start_time", "end_time"]
        widgets = {
            "start_datetime": forms.SplitDateTimeWidget(),
            "end_datetime": forms.SplitDateTimeWidget(),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []
