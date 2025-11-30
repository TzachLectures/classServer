from django.shortcuts import render
from .models import Book,Author
from django.http import JsonResponse

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    data =[]
    for b in books:
        data.append({
            "title":b.title,
            "pages":b.pages,
            "author":b.author,
            "year":b.year
        })
    
    return JsonResponse(data,safe=False)

def list_authors(request):
    authors = Author.objects.all()
    data =[]
    for a in authors:
        data.append({
            "name":a.name,
            "email":a.email,
            "birth_year":a.birth_year
        })
    
    return JsonResponse(data,safe=False)