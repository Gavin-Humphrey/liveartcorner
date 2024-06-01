from django.contrib import admin
from services.models import Service

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = ['name', 'description', 'duration', 'price']
    readonly_fields = ['name', 'description', 'duration', 'price']

admin.site.register(Service)
