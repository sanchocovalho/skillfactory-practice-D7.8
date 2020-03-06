from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from p_library.models import Author, Book, Publisher, Friend
from p_library.forms import AuthorForm, BookForm, PublisherForm, FriendForm, UserRegistrationForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms import formset_factory  
# from django.http.response import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from allauth.account.views import LogoutView
from allauth.socialaccount.models import SocialAccount

class MyLogoutView(LogoutView):
    template_name = 'logout.html'

class AuthorUpdate(UpdateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = 'author_edit.html'

class AuthorCreate(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = 'author_edit.html'

class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('p_library:book_list')
    template_name = 'book_edit.html'

class BookCreate(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('p_library:book_list')
    template_name = 'book_edit.html'

class PublisherUpdate(UpdateView):
    model = Publisher
    form_class = PublisherForm
    success_url = reverse_lazy('p_library:publisher_list')
    template_name = 'publisher_edit.html'

class PublisherCreate(CreateView):
    model = Publisher
    form_class = PublisherForm
    success_url = reverse_lazy('p_library:publisher_list')
    template_name = 'publisher_edit.html'

class FriendUpdate(UpdateView):
    model = Friend
    form_class = FriendForm
    success_url = reverse_lazy('p_library:friend_list')
    template_name = 'friend_edit.html'

class FriendCreate(CreateView):
    model = Friend
    form_class = FriendForm
    success_url = reverse_lazy('p_library:friend_list')
    template_name = 'friend_edit.html'

def log_in(request, template_html):     
    context = {}
    if request.method == 'POST':
        template = loader.get_template(template_html)
        if 'btnSignIn' in request.POST:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                login(request, authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password']))
                return render(request, template_html)
            else:
                msg_data = {"errmsg": "Введите логин и пароль ещё раз!"}
                return HttpResponse(template.render(msg_data, request))     
        else:
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                auth.login(request, form.get_user())
            else:
                msg_data = {"errmsg": "Неверный логин или пароль!"}
                return HttpResponse(template.render(msg_data, request))
        return render(request, template_html)
    else:
        context['form'] = AuthenticationForm()

    return render(request, template_html, context)

def get_extra_data(request):
    github_url = None
    if SocialAccount.objects.filter(provider='github', user=request.user).exists():
        github_url = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']
    return github_url

def book_list(request):
    if request.user.is_authenticated:
        template = loader.get_template('book_list.html')
        books = Book.objects.all()
        github_url = get_extra_data(request)
        biblio_data = {
            "books": books,
            "github_url": github_url,
        }
        return HttpResponse(template.render(biblio_data, request))
    return log_in(request, 'book_list.html')

def author_list(request):
    if request.user.is_authenticated:
        template = loader.get_template('author_list.html')
        authors = Author.objects.all()
        github_url = get_extra_data(request)
        biblio_data = {
            "authors": authors,
            "github_url": github_url,
        }
        return HttpResponse(template.render(biblio_data, request))
    return log_in(request, 'author_list.html')

def publisher_list(request):
    if request.user.is_authenticated:
        template = loader.get_template('publisher_list.html')
        publishers = Publisher.objects.all()
        github_url = get_extra_data(request)
        biblio_data = {
            "publishers": publishers,
            "github_url": github_url,
        }
        return HttpResponse(template.render(biblio_data, request))
    return log_in(request, 'publisher_list.html')

def friend_list(request):
    if request.user.is_authenticated:
        template = loader.get_template('friend_list.html')
        friends = Friend.objects.all()
        github_url = get_extra_data(request)
        biblio_data = {
            "friends": friends,
            "github_url": github_url,
        }
        return HttpResponse(template.render(biblio_data, request))
    return log_in(request, 'friend_list.html')

def library(request):
    if request.user.is_authenticated:
        template = loader.get_template('library.html')
        books = Book.objects.all()
        friends = Friend.objects.all()
        github_url = get_extra_data(request)
        biblio_data = {
            "title": "мою библиотеку",
            "books": books,
            "friends": friends,
            "github_url": github_url,  
        }
        return HttpResponse(template.render(biblio_data, request))
    return log_in(request, 'library.html')

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/library/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/library/')
            book.copy_count += 1
            book.save()
        return redirect('/library/')
    else:
        return redirect('/library/')

def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/library/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/library/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/library/')
    else:
        return redirect('/library/')

def borrowed_book(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        friend_id = request.POST['select_borrowed']
        if not book_id:
            return redirect('/library/')
        else:
            book = Book.objects.filter(id=book_id).first()
            friend = Friend.objects.get(id=friend_id)
            if not book:
                return redirect('/library/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
                book.borrowed_book_count += 1
                book.friend.add(friend)
            book.save()
        return redirect('/library/')
    else:
        return redirect('/library/')

def returned_book(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        friend_id = request.POST['select_returned']
        if not book_id:
            return redirect('/library/')
        else:
            book = Book.objects.filter(id=book_id).first()
            friend = Friend.objects.get(id=friend_id)
            if not book:
                return redirect('/library/')
            if book.borrowed_book_count < 1:
                book.borrowed_book_count = 0
            else:
                book.copy_count += 1
                book.borrowed_book_count -= 1
                book.friend.remove(friend)
            book.save()
        return redirect('/library/')
    else:
        return redirect('/library/')
