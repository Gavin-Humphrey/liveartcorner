from django.contrib import admin
from django import forms
from .models import User
from base.forms import CustomUserChangeForm


# def vet_artists(modeladmin, request, queryset):
#     queryset.update(is_vetted_artist=True)
    
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['email', 'name', 'is_artist', 'is_vetted_artist']
#     actions = [vet_artists]
# admin.site.register(User, UserAdmin)


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