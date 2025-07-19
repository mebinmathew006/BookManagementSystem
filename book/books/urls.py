from django.urls import path
from .views import UserUploadBook



urlpatterns = [
    path('upload',UserUploadBook.as_view() , name= 'upload'),
     
]