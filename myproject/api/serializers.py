from rest_framework import serializers
from .models import Book,Author,Category,UserProfile
from django.contrib.auth.models import User
from django.db import transaction


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields="__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields="__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields="__all__"




class BookWithAuthorSerializer(serializers.ModelSerializer):
    author=AuthorSerializer()
    class Meta:
        model = Book
        fields="__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = UserProfile
        fields= "username","password", "primary_phone", "secondary_phone", "city", "street", "birth_date"
    
    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data.pop("username"),
                password=validated_data.pop("password"),
            )

            profile = UserProfile.objects.create(user=user,**validated_data)
        return profile
       
