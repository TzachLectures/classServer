from django.contrib import admin
from .models import Book , Author,Category,UserProfile,Product

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Product)