from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    re_path(r'^books/$', views.BookListView.as_view(), name='books-list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    re_path(r'^books/create/$', views.BookCreate.as_view(), name='books_create'),
    re_path(r'^books/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='books_update'),
    re_path(r'^books/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='books_delete'),
]

urlpatterns += [
    path('authors/', views.AuthorListView.as_view(), name='authors-list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    re_path(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    re_path(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.RenewBookLibrarian.as_view(), name='renew-book-librarian'),
]
