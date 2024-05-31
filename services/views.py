from django.shortcuts import render, redirect
from django.contrib import messages
from base.forms import ServiceForm
from services.models import Service

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully!")
            return redirect('artist-dashboard', user_id=request.user.id)  # Redirect to the artist dashboard view
        else:
            messages.error(request, "There was an error adding the service.")
    else:
        form = ServiceForm()
    return render(request, 'service/add_service.html', {'form': form})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'service/services_list.html', {'services': services})

def service_detail(request, service_id):
    service = Service.objects.get(pk=service_id)
    return render(request, 'services/service_detail.html', {'service': service})