from django.contrib import admin
from services.models import Service, Booking


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = ["name", "description", "duration", "price"]
    readonly_fields = ["name", "description", "duration", "price"]


admin.site.register(Service)


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ["user", "availability", "service", "created_at"]
    readonly_fields = ["user", "availability", "service", "created_at"]


admin.site.register(Booking)
