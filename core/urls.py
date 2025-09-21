from django.urls import path 
from .views import *

urlpatterns = [
    path('customer', CustomerView.as_view()),
]
