from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_year = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    pages = models.IntegerField()
    year=models.IntegerField()
    is_best_seller =models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name="books")
    categories = models.ManyToManyField(Category,related_name="books")

    def __str__(self):
        return self.title


class UserProfile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    primary_phone = models.CharField(max_length=20, blank=True)
    secondary_phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


