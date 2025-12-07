from .models import Book,Author
from .serializers import BookSerializer,AuthorSerializer,BookWithAuthorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.

@api_view(["GET","POST"])
def list_books(request):
    if request.method=="GET":
        books = Book.objects.all()
        serializer = BookWithAuthorSerializer(books,many=True)
        return Response(serializer.data)
    if request.method=="POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
def book_details(request,id):
    try:
        book = Book.objects.get(pk=id)

        if request.method=="GET":
            serializer = BookWithAuthorSerializer(book)
            return Response(serializer.data)
        if request.method =="DELETE":
            book.delete()
            return Response({'message': 'Book deleted successfully'}, status=204)
        if request.method=="PUT":
            serializer = BookSerializer(book,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    except Book.DoesNotExist:
        return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def books_by_year(request,year):
    books = Book.objects.filter(year=year)
    serializer = BookWithAuthorSerializer(books,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def books_by_author(request,author):
    books = Book.objects.filter(author__name=author)
    serializer = BookWithAuthorSerializer(books,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def books_by_author_birth_year(request,year):
    books = Book.objects.filter(author__birth_year__gte=year)
    serializer = BookWithAuthorSerializer(books,many=True)
    return Response(serializer.data)


@api_view(["GET"])
def author_details(request,id):
        author = get_object_or_404(Author,pk=id)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)



@api_view(["GET","POST"])
def list_authors(request):
    if request.method=="GET":
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors,many=True)
        return Response(serializer.data)
    if request.method=="POST":
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



