from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class Register(models.Model):
#     fullname=models.CharField(max_length=30,null=True)
#     email=models.EmailField(max_length=30,null=True)
#     password=models.CharField(max_length=30,null=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class AddBooks(models.Model):
    name = models.CharField(max_length=25,null=True)
    img = models.ImageField(null=True)
    description = models.TextField(null=True)
    author = models.CharField(max_length=255,null=True)
    genre = models.CharField(max_length=100,null=True)
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    book = models.ForeignKey(AddBooks, on_delete=models.CASCADE,null=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
class Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book_id = models.ForeignKey(AddBooks,on_delete=models.CASCADE,null=True)
    openlibrary_key = models.CharField(max_length=255, null=True, blank=True)  # Store the Open Library book key
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    cover_id = models.IntegerField(null=True, blank=True)  # Store cover ID for easy display
