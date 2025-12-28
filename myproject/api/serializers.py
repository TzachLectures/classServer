from rest_framework import serializers
from .models import Book,Author,Category,UserProfile


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
    class Meta:
        model = UserProfile
        fields= "primary_phone", "secondary_phone", "city", "street", "birth_date"