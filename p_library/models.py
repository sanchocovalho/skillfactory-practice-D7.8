from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    def __str__(self):
        return self.user.username

class Author(models.Model):
    full_name = models.TextField()  
    birth_year = models.SmallIntegerField()  
    country = models.CharField(max_length=2)
    def __str__(self):
        return self.full_name

class Publisher(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name

class Friend(models.Model):
    full_name = models.TextField()
    def __str__(self):
        return self.full_name

class Book(models.Model):  
    ISBN = models.CharField(max_length=13)  
    title = models.TextField()  
    description = models.TextField()  
    year_release = models.SmallIntegerField()  
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
        )
    copy_count = models.SmallIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='books'
        )
    friend = models.ManyToManyField(
        Friend,
        blank=True,
        related_name='friends'
        )
    borrowed_book_count = models.SmallIntegerField(default=0)
    cover = models.ImageField(
        verbose_name='Обложка',
        upload_to='covers',
        blank=True
        )
    def __str__(self):
        return self.title
