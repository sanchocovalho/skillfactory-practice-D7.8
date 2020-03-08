from django.urls import path, re_path
from django.conf.urls import url
from p_library import views
from allauth.account.views import login

app_name = "p_library"

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('update/profile', views.edit_profile, name='user_edit'),
    path('login/', login, name='login'),  
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('create', views.BookCreate.as_view(), name="book_create"),
    path("update<int:pk>", views.BookUpdate.as_view(), name="book_update"),
    path('library/', views.library, name='library'),
    path('library/book_increment/', views.book_increment),
    path('library/book_decrement/', views.book_decrement),
    path('library/borrowed_book/', views.borrowed_book),
    path('library/returned_book/', views.returned_book),
    path('authors/', views.author_list, name='author_list'),
    path('authors/create', views.AuthorCreate.as_view(), name='author_create'),
    path("authors/update<int:pk>", views.AuthorUpdate.as_view(), name="author_update"),
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/create', views.PublisherCreate.as_view(), name='publisher_create'),
    path("publishers/update<int:pk>", views.PublisherUpdate.as_view(), name="publisher_update"),
    path('friends/', views.friend_list, name='friend_list'),
    path('friends/create', views.FriendCreate.as_view(), name='friend_create'),
    path("friends/update<int:pk>", views.FriendUpdate.as_view(), name="friend_update"),
]
