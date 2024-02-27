from django.urls import path
from construct2lsapp import views

urlpatterns = [
    path('', views.index, name="index")

]