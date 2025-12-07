from django.urls import path
from .views import list_books,list_authors,book_details,author_details,books_by_year,books_by_author,books_by_author_birth_year

urlpatterns = [
    path("books/", list_books),
    path("books/<int:id>/",book_details),
    path("books/year/<int:year>/",books_by_year),
    path("books/author/<str:author>/",books_by_author),
    path("books/author/year/<int:year>/",books_by_author_birth_year),
    path("authors/", list_authors),
    path("authors/<int:id>/", author_details),
]
