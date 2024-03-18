from django.urls import path
from construct2lsapp import views

# Define urlpatterns to map URLs to views

urlpatterns = [
    # Home page
    path('', views.index, name="index"),

    # Contact page
    path('contact', views.contact, name="contact"),

    # About page
    path('about', views.about, name="about"),

    # Profile page
    path('profile', views.profile, name="profile"),

    # Blog page
    path('blog', views.blog, name="blog"),

    # Checkout page
    path('checkout/', views.checkout, name="checkout"),

    # Endpoint for handling requests (e.g., payment)
    path('handlerequest/', views.handlerequest, name="handlerequest"),
]
