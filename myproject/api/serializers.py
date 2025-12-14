from rest_framework import serializers
from .models import Book,Author,Category


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
        fields=["id","title","pages","year","author"]

    def validate_pages(self,value):
        if value<10:
            raise serializers.ValidationError("לא ניתן להכניס ספר הקצר מ10 עמודים")
        return value

    def validate_title(self,value):
        forbidden=['test', 'temp', 'check', 'admin', 'null']
        if value.lower() in forbidden:
            raise serializers.ValidationError(f"'{value}' is not allowed as a book title.")
        return value
    
    def validate(self,data):
        new_title=data.get("title")
        if len(new_title)<2:
            raise serializers.ValidationError("לא ניתן להכניס ספר עם כותרת הקצרה מ2 תווים")
        new_pages=data.get("pages")
        if (new_title[0]=="a" or new_title[0]=="A") and new_pages<25:
            raise serializers.ValidationError("לא ניתן להכניס ספר עם כותרת שמתחילה באות a/A וגם שיהיה קצר מ25 עמודים")

        return data




class BookWithAuthorSerializer(serializers.ModelSerializer):
    author=AuthorSerializer()
    class Meta:
        model = Book
        fields=["id","title","pages","year","author","categories"]


