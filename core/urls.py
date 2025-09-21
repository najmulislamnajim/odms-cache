from django.urls import path 
from .views import *

urlpatterns = [
    path('customer', CustomerView.as_view()),
    path('material', MaterialView.as_view()),
    path('da', UsersListView.as_view()),
]
