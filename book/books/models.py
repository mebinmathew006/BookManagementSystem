from django.db import models
from django.contrib.auth import get_user_model
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

User = get_user_model()

class Books(models.Model):
    title = models.CharField( max_length=50)
    book = models.ImageField(upload_to='books/',storage=MediaCloudinaryStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    author = models.CharField( max_length=50)
    genre = models.CharField( max_length=50)
    publication_date = models.DateField()
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.title} by {self.author}"

    