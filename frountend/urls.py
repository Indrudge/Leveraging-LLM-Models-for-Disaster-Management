from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='home'),
    path('home',views.index,name='home'),
    path('disaster/', views.disaster_news, name='disaster_news'),
    path('map',views.map,name='map'),
    path('about', views.about,name='about'),
    path('contact', views.contact,name='contact'),
    path('disasterlist', views.disasterlist,name='disasterlist'),
    path('disasterd/', views.disaster_detail, name='disasterdetail'), # Route to specific disaster details
    path("contact-us/", views.contact_us, name="contact_us"),
]
