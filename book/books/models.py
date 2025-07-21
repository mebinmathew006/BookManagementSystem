from django.db import models
from django.contrib.auth import get_user_model
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

User = get_user_model()

class Books(models.Model):
    title = models.CharField( max_length=50)
    book = models.FileField(upload_to='books/',storage=MediaCloudinaryStorage())
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    genre = models.CharField( max_length=50)
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    
class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='readinglists')
    name = models.CharField(max_length=100)  
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    
class ReadingItem(models.Model):
    readinglist = models.ForeignKey(ReadingList,on_delete=models.CASCADE,related_name='readingitems')
    book = models.ForeignKey(Books,on_delete=models.CASCADE,related_name='readingitems')
    order = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('readinglist', 'order')
        ordering = ['order']  

    def __str__(self):
        return f"{self.book.title} in list {self.readinglist.id} at position {self.order}"