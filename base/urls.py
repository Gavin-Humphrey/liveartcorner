from django.urls import path
from . import views
from base.views import home


urlpatterns = [
    path("", home, name="home"),
    path("contact", views.contact, name="contact"),

    path('faq/', views.faq, name='faq'),
    path('about-us/', views.about_us, name='about-us'),
    path('terms-conditions/', views.terms_conditions, name='terms-conditions'),
    path('our-services/', views.our_services, name='our-services'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('affiliate-program/', views.affiliate_program, name='affiliate-program'),
]
