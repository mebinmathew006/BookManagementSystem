from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from cloudinary_storage.storage import MediaCloudinaryStorage

class UserManger(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        return self.create_user(email, password, **extra_fields)
        

class User(AbstractBaseUser):
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profile_images/',storage=MediaCloudinaryStorage())
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['profile_image','name']
    
    objects = UserManger()
        
    