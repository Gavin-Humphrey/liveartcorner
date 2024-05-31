from django.contrib import admin

from .models import Service



class ServiceAdmin(admin.ModelAdmin):
    model = Service
    extra = 0
    fields = ['user',]
    list_display = ['name', 'description', 'price']
admin.site.register(Service, ServiceAdmin)

