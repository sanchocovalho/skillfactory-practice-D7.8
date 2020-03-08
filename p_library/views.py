from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from p_library.models import Author, Book, Publisher, Friend, UserProfile
from p_library.forms import AuthorForm, BookForm, PublisherForm, FriendForm, \
                            UserRegistrationForm, UserForm, UserProfileForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from allauth.account.views import LogoutView
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class MyLogoutView(LogoutView):
    template_name = 'logout.html'

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        print(profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/')
    else:
        user_form = UserForm(instance=request.user)
        try:
            profile_form = UserProfileForm(instance=request.user.profile)
        except:
            profile_form = UserProfileForm(instance=UserProfile.objects.create(user=request.user))
        print(profile_form)
    return render(request, 'user_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

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

def log_in(request, template, context):     
    if request.method == 'POST':
        if 'btnSignIn' in request.POST:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                login(request, authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password']))
            else:
                context['errmsg'] = "Введите логин и пароль ещё раз!"     
        else:
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                auth.login(request, form.get_user())
            else:
                context['errmsg'] = "Неверный логин или пароль!"
    else:
        context['form'] = AuthenticationForm()
    return HttpResponse(template.render(context, request))

def get_extra_data(request):
    try:
        github_url = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']
    except:
        github_url = None
    return github_url

def book_list(request):
    template = loader.get_template('book_list.html')
    books = Book.objects.all()
    github_url = get_extra_data(request)
    context = {
        "books": books,
        "github_url": github_url,
    }
    if request.user.is_authenticated:
        return HttpResponse(template.render(context, request))
    return log_in(request, template, context)

def author_list(request):
    template = loader.get_template('author_list.html')
    authors = Author.objects.all()
    github_url = get_extra_data(request)
    context = {
        "authors": authors,
        "github_url": github_url,
    }
    if request.user.is_authenticated:
        return HttpResponse(template.render(context, request))
    return log_in(request, template, context)

def publisher_list(request):
    template = loader.get_template('publisher_list.html')
    publishers = Publisher.objects.all()
    github_url = get_extra_data(request)
    context = {
        "publishers": publishers,
        "github_url": github_url,
    }
    if request.user.is_authenticated:
        return HttpResponse(template.render(context, request))
    return log_in(request, template, context)

def friend_list(request):
    template = loader.get_template('friend_list.html')
    friends = Friend.objects.all()
    github_url = get_extra_data(request)
    context = {
        "friends": friends,
        "github_url": github_url,
    }
    if request.user.is_authenticated:
        return HttpResponse(template.render(context, request))
    return log_in(request, template, context)

def library(request):
    template = loader.get_template('library.html')
    books = Book.objects.all()
    friends = Friend.objects.all()
    github_url = get_extra_data(request)
    context = {
        "title": "мою библиотеку",
        "books": books,
        "friends": friends,
        "github_url": github_url,  
    }
    if request.user.is_authenticated:
        return HttpResponse(template.render(context, request))
    return log_in(request, template, context)

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
