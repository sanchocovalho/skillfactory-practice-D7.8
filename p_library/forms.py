from django import forms  
from p_library.models import Author, Book, Publisher, Friend, UserProfile
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

    username = forms.CharField(
        label='Логин',
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите новый логин'
            }
        )
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }
        )
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }
        )
    )

    email = forms.EmailField(
        label='Электронная почта',
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите электронную почту'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    country = forms.CharField(
        label='Страна',
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите страну'
            }
        )
    )

    location = forms.CharField(
        label='Город',
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите город'
            }
        )
    )

    birth_date = forms.DateField(
        label='Дата рождения',
        required=False,
        input_formats=['%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите дату рождения в формате ДД.ММ.ГГГГ'
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = ('country', 'location', 'birth_date')

class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
        )

    class Meta:
        model = User
        fields = ('username',)

class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Текущяя'
    input_text = 'Изменить'
    clear_checkbox_label = 'Удалить'

class AuthorForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Имя автора',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите имя автора'
            }
        )
    )
    birth_year = forms.CharField(
        label='Дата рождения автора',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите дату рождения автора'
            }
        )
    )
    country = forms.CharField(
        label='Страна происхождения',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите страну'
            }
        )
    )
    class Meta:
        model = Author
        fields = '__all__'

class BookForm(forms.ModelForm):
    ISBN = forms.CharField(
        label='ISBN',
        widget=forms.TextInput(
            attrs={
                'required': True,
                'type':'number',
                'class': 'form-control',
                'placeholder': 'Введите ISBN = 13 чисел'
            }
        )
    )
    title = forms.CharField(
        label='Название книги',
        widget=forms.TextInput(
            attrs={
                'required': True,
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите название книги'
            }
        )
    )
    description = forms.CharField(
        label='Описание книги',
        widget=forms.Textarea(
            attrs={
                'required': True,
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание книги'
            }
        )
    )
    year_release = forms.CharField(
        label='Дата публикации',
        widget=forms.TextInput(
            attrs={
                'required': True,
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Введите дату создания книги'
            }
        )
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label='Автор книги',
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control'
            }
        )
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        label='Издательство',
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control'
            }
        )
    )
    copy_count = forms.CharField(
        label= 'Общее количество книг',
        widget= forms.TextInput(
            attrs={
                'required': True,
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Введите общее количество книг'
            }
        )
    )
    price = forms.CharField(
        label= 'Цена книги',
        widget= forms.TextInput(
            attrs={
                'required': True,
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Введите стоимость книги'
            }
        )
    )
    cover = forms.ImageField(
        label= 'Обложка',
        required=False,
        widget= MyClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': '.jpg,.jpeg,.png,.gif'
            }
        )
    )
    class Meta:
        model = Book
        fields = ('ISBN', 'title', 'description', 'year_release', 'author', 'price', 'copy_count', 'publisher', 'cover')

class PublisherForm(forms.ModelForm):
    name = forms.CharField(
        label='Издательство',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите название издательства'
            }
        )
    )
    class Meta:
        model = Publisher
        fields = '__all__'

class FriendForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Имя друга',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите имя друга'
            }
        )
    )
    class Meta:
        model = Friend
        fields = '__all__'
