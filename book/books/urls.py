from django.urls import path
from .views import UserUploadBook,UserReadingList



urlpatterns = [
    path('upload',UserUploadBook.as_view() , name= 'upload'),
    path('upload/<int:book_id>/', UserUploadBook.as_view(), name='delete-book'),
    path('readinglist',UserReadingList.as_view() , name= 'readinglist'),
    path('readinglist/<int:list_id>/', UserReadingList.as_view(), name='delete-readinglist'),
]