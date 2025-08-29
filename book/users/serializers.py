from rest_framework import serializers
from .models import User
import re


class UserSignupSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'profile_image', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_name(self,value):
        if not re.match(r'^[A-Za-z\s]+$', value):  
            raise serializers.ValidationError("Name must contain only letters and spaces.")
        return value
    
    def validate_email(self, value):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[^A-Za-z0-9]', value):   
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)
    
    class Meta :
         fields = ['email','password' ]
         
         
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField()
    class Meta:
        model = User
        fields = ['name', 'profile_image']
        
        
    def validate_name(self,value):
        print(value)
        if not re.match(r'^[A-Za-z\s]+$', value):  
            raise serializers.ValidationError("Name must contain only letters and spaces.")

        return value