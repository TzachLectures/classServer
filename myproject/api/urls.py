from django.urls import path
from .views import list_books,list_authors,book_details,author_details,books_by_year,books_by_author,books_by_author_birth_year,add_category_to_book,remove_category_to_book

urlpatterns = [
    path("books/", list_books),
    path("books/<int:id>/",book_details),
    path("books/year/<int:year>/",books_by_year),
    path("books/author/<str:author>/",books_by_author),
    path("books/author/year/<int:year>/",books_by_author_birth_year),
    path("books/category/<int:book_id>/",add_category_to_book),
    path("books/category/remove/<int:book_id>/",remove_category_to_book),
    path("authors/", list_authors),
    path("authors/<int:id>/", author_details),
]
