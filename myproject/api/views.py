from .models import Book,Author,Category
from .serializers import BookSerializer,AuthorSerializer,BookWithAuthorSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.

@api_view(["GET","POST"])
def list_books(request):
    year = request.query_params.get("year")
    pages = request.query_params.get("pages")
    q=request.query_params.get("q")

    if request.method=="GET" and q:
        query = Q(title__icontains=q) | Q(author__name__icontains=q)
        books = Book.objects.filter(query)
        serializer = BookWithAuthorSerializer(books,many=True)
        return Response(serializer.data)
    if request.method=="GET" and year and pages:
        query = Q(year__gt=year) | Q(pages__gt=pages)
        books = Book.objects.filter(query)
        serializer = BookWithAuthorSerializer(books,many=True)
        return Response(serializer.data)
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
def books_by_category(request,categoryId):
    #Solution 1
    # category = get_object_or_404(Category,pk=categoryId)
    # books_from_this_category = category.books
    # serializer = BookWithAuthorSerializer(books_from_this_category,many=True)

    #Solution 2
    books_from_this_category= Book.objects.filter(categories__id=categoryId)
    serializer = BookWithAuthorSerializer(books_from_this_category,many=True)
    return Response(serializer.data)



@api_view(["POST"])
def add_category_to_book(request,book_id):
    book = get_object_or_404(Book,pk=book_id)
    cat_id = request.data.get("category_id")
    category = get_object_or_404(Category,pk=cat_id)
    book.categories.add(category)
    return Response({'message': f'Category {category.name} added to {book.title}'})

@api_view(["POST"])
def remove_category_to_book(request,book_id):
    book = get_object_or_404(Book,pk=book_id)
    cat_id = request.data.get("category_id")
    category = get_object_or_404(Category,pk=cat_id)
    book.categories.remove(category)
    return Response({'message': f'Category {category.name} removed from {book.title}'})



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


@api_view(["GET","POST"])
def list_categories(request):
    if request.method=="GET":
        authors = Category.objects.all()
        serializer = CategorySerializer(authors,many=True)
        return Response(serializer.data)
    if request.method=="POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Sum,Count

@api_view(["GET"])
def getTotalPages(request):
    sumPages = Book.objects.aggregate(total_pages=Sum("pages"))
    return Response(sumPages)


@api_view(["GET"])
def authors_books(request):
    authors = Author.objects.annotate(num_books=Count("books"))
    data = []
    for author in authors:
        data.append({
            'name':author.name,
            "books_count":author.num_books
        })

    return Response(data)