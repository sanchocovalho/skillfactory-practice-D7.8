from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,
        verbose_name=u'Пользователь',
        on_delete=models.CASCADE,
        related_name='profile'
        )
    country = models.CharField(
        verbose_name=u'Страна',
        max_length=50,
        blank=True
        )
    location = models.CharField(
        verbose_name=u'Город',
        max_length=30,
        blank=True
        )
    birth_date = models.DateField(
        verbose_name=u'Дата рождения',
        null=True,
        blank=True
        )

    class Meta:
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Данные пользователей'

    def __str__(self):
        return self.user.username

class Author(models.Model):
    full_name = models.TextField(
        verbose_name=u'Имя'
        )  
    birth_year = models.SmallIntegerField(
        verbose_name=u'Год рождения'
        )  
    country = models.CharField(
        verbose_name=u'Страна',
        max_length=2
        )

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.full_name

class Publisher(models.Model):
    name = models.TextField(
        verbose_name=u'Название'
        )

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'

    def __str__(self):
        return self.name

class Friend(models.Model):
    full_name = models.TextField(
        verbose_name=u'Имя'
        )

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return self.full_name

class Book(models.Model):  
    ISBN = models.CharField(max_length=13)  
    title = models.TextField(
        verbose_name=u'Название'
        )  
    description = models.TextField(
        verbose_name=u'Описание'
        )  
    year_release = models.SmallIntegerField(
        verbose_name=u'Год выпуска'
        )  
    author = models.ForeignKey(
        Author,
        verbose_name=u'Автор',
        on_delete=models.CASCADE
        )
    copy_count = models.SmallIntegerField(
        verbose_name=u'Количество',
        default=1
        )
    price = models.DecimalField(
        verbose_name=u'Цена',
        max_digits=6,
        decimal_places=2
        )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        verbose_name=u'Издательство',
        null=True,
        blank=True,
        related_name='books'
        )
    friend = models.ManyToManyField(
        Friend,
        verbose_name=u'Друг',
        blank=True,
        related_name='books'
        )
    borrowed_book_count = models.SmallIntegerField(
        verbose_name=u'Количество одолженных',
        default=0
        )
    cover = models.ImageField(
        verbose_name=u'Обложка',
        upload_to='covers',
        blank=True
        )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
