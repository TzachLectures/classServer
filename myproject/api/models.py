from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_year = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=200)
    pages = models.IntegerField()
    year=models.IntegerField()
    is_best_seller =models.BooleanField(default=False)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name="books")
    categories = models.ManyToManyField(Category,related_name="books")

    def __str__(self):
        return self.title





