from django.urls import path, include
from app import views

urlpatterns = [
    path('get-data/', views.GetData.as_view(), name='get-data'),
]