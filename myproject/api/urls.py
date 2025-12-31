from django.urls import path
from .views import list_books,list_authors,book_details,author_details,books_by_year,books_by_author,books_by_author_birth_year,add_category_to_book,remove_category_to_book,list_categories,books_by_category,getTotalPages,authors_books,predict_book_price,register
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("books/", list_books),
    path("books/<int:id>/",book_details),
    path("books/year/<int:year>/",books_by_year),
    path("books/author/<str:author>/",books_by_author),
    path("books/author/year/<int:year>/",books_by_author_birth_year),
    path("books/category/<int:book_id>/",add_category_to_book),
    path("books/category/remove/<int:book_id>/",remove_category_to_book),
    path("books/bycategory/<int:categoryId>/",books_by_category),
    path("authors/", list_authors),
    path("authors/<int:id>/", author_details),
    path("categories/",list_categories),
    path("sumpages/",getTotalPages),
    path("authorsbooks/",authors_books),
    path("predict/",predict_book_price),
    path("users/register/",register),
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
