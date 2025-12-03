from rest_framework import serializers
from .models import Book,Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields="__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=["id","title","pages","year","author"]

class BookWithAuthorSerializer(serializers.ModelSerializer):
    author=AuthorSerializer()
    class Meta:
        model = Book
        fields=["id","title","pages","year","author"]


