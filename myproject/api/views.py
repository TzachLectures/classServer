from .models import Book,Author
from .serializers import BookSerializer,AuthorSerializer,BookWithAuthorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
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



