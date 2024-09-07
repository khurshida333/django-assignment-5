from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True,null=True,blank=True) #slug
    content = models.TextField()
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  #ex: 20000.00
    borrower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='borrowed_books', blank=True,null=True)
    category = models.ManyToManyField(Category)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='book_posts/media/uploads/', blank = True, null = True)
    is_borrowed = models.BooleanField(default=False)
    def __str__(self):
        return  self.title
    

class Review(models.Model): 
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models. DateTimeField(auto_now_add=True) # jkhn e ei class er object toiri

    def __str__(self):
       return f"Comments by {self.name}"
    

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who borrowed the book
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # The borrowed book
    borrowed_date = models.DateTimeField(auto_now_add=True)  # Automatically set the date when the book is borrowed

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} on {self.borrowed_date}"