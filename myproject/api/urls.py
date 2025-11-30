from django.urls import path
from .views import list_books,list_authors

urlpatterns = [
    path("books/", list_books),
    path("authors/", list_authors),

]
