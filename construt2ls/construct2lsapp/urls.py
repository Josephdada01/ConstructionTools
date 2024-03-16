from django.urls import path
from construct2lsapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('profile', views.profile, name="profile"),
    path('blog', views.blog, name="blog"),
    path('checkout/', views.checkout, name="checkout"),
    path('handlerequest/', views.handlerequest, name="handlerequest"),

]