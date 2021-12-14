from django.urls import path
from . import views

from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    url(r'^books/$', views.BookListView.as_view(), name='books-list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [
    path('authors/', views.AuthorListView.as_view(), name='authors-list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]
