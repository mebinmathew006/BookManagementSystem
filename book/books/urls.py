from django.urls import path
from .views import UserUploadBook,UserReadingList,UserReadingListItem

urlpatterns = [
    path('books', UserUploadBook.as_view(), name= 'upload'),
    path('books/<int:book_id>', UserUploadBook.as_view(), name='delete-book'),
    path('reading-list/', UserReadingList.as_view(), name= 'readinglist'),
    path('reading-list/<int:list_id>/', UserReadingList.as_view(), name='delete_or_update-readinglist'),
    path('reading-item/<int:list_id>/', UserReadingListItem.as_view(), name='readinglistitem'),
]