"""
URL configuration for liveartcorner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.shortcuts import redirect  ####


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("user/", include("user.urls")),
    path("", include("dashboard.urls")),
    path("", include("item.urls")),
    path("", include("cart.urls")),
    path("", include("wishlist.urls")),
    path("", include("order.urls")),
    path("", include("services.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("contact/", include("django_secure_contact_form.urls")),  # Use plugin's URL
    path("captcha/", include("captcha.urls")),  # Include CAPTCHA URLs
    path("", lambda request: redirect("contact")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(
            r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
        ),
    ]
