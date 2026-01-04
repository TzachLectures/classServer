from .models import Book,Author,Category
from .serializers import BookSerializer,AuthorSerializer,BookWithAuthorSerializer,CategorySerializer,UserProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListCreateAPIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from decouple import config
# Create your views here.


@api_view(["POST"])
def register(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
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


@api_view(["POST"])
def predict_book_price(request):
    is_best_seller = request.data.get("is_best_seller")
    pages = request.data.get("pages")

    df = pd.read_json(r'C:\Users\benny\Desktop\האקריו\W271024ER\django\class3\projectFromGit\classServer\myproject\api\modelData\books.json')    # 1. הסרת עמודת id
    df = df.drop('id', axis=1)

    # 2. פירוק עמודת author לעמודות author_id ו-author_birth_year והסרת עמודת author המקורית
    # נשתמש ב-get כדי למנוע שגיאות אם המפתח אינו קיים (לדוגמה, birth_year לא הופיע ב-head() הקודם)
    df['author_id'] = df['author'].apply(lambda x: x.get('id'))
    df['author_birth_year'] = df['author'].apply(lambda x: x.get('birth_year'))
    df = df.drop('author', axis=1)

    # 3. הסרת עמודת title
    df = df.drop('title', axis=1)

    # 4. המרת עמודת is_best_seller לבוליאנית למספרים (1 או 0)
    df['is_best_seller'] = df['is_best_seller'].astype(int)


    author_id_encoded = pd.get_dummies(df['author_id'], prefix='author_id')
    df = pd.concat([df, author_id_encoded], axis=1)
    df.drop('author_id', axis=1, inplace=True)

    unique_categories = set()
    for categories_list in df['categories']:
        if isinstance(categories_list, list):
            for category_id in categories_list:
                unique_categories.add(category_id)

    for category_id in sorted(list(unique_categories)):
        df[f'category_{category_id}'] = df['categories'].apply(lambda x: 1 if isinstance(x, list) and category_id in x else 0)

    df = df.drop('categories', axis=1)  

    for col in df.columns:
        if col.startswith('author_id_'):
            df[col] = df[col].astype(int)

    x = df[['is_best_seller', 'pages']]
    y = df[["price"]]   

    x_scaler = MinMaxScaler()
    x_scaled = x_scaler.fit_transform(x)

    y_scaler = MinMaxScaler()
    y_scaled = y_scaler.fit_transform(y)



    X_train, X_test, y_train, y_test = train_test_split(x_scaled, y_scaled, test_size=0.3, random_state=1234)
    model = LinearRegression()
    model.fit(X_train,y_train)


        # יצירת DataFrame חדש עם הקלט
    new_book_data = pd.DataFrame({
        'is_best_seller': [is_best_seller],
        'pages': [pages]
    })
     # סקאלינג של הנתונים החדשים באמצעות הסקיילר שאומן בעבר
    scaled_new_book_data = x_scaler.transform(new_book_data)
    # חיזוי המחיר המוסקל
    predicted_price_scaled = model.predict(scaled_new_book_data)

    # החזרת המחיר המוסקל למחיר המקורי
    predicted_price = y_scaler.inverse_transform(predicted_price_scaled)

    return Response( {"price": predicted_price[0][0]})



class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'description','category']
    search_fields = ['name', 'description','category']
    ordering_fields = ['price', 'quantity']
    ordering = ['-price']




class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET"])
def example_for_env_variables(request):
    app_name = config("APPNAME",default="Default App Name")
    return Response({"message": app_name})