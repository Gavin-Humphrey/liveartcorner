from django.contrib import admin
from django import forms
from .models import User, ArtistAvailability
from base.forms import CustomUserChangeForm



def vet_artists(modeladmin, request, queryset):
    queryset.update(is_vetted_artist=True)

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    list_display = ['email', 'name', 'is_artist', 'is_vetted_artist']
    actions = [vet_artists]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_artist', 'is_vetted_artist', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)


class ArtistAvailabilityInline(admin.TabularInline):
    model = ArtistAvailability
    extra = 0
    fields = ['artist', 'date', 'start_time', 'end_time']
    readonly_fields = ['artist', 'date', 'start_time', 'end_time']

admin.site.register(ArtistAvailability)