from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('book/', include([
        path('', views.BookListView.as_view(), name='books-list'),
        path('<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

        path(r'create/', views.BookCreate.as_view(), name='books_create'),
        path(r'<int:pk>/update/', views.BookUpdate.as_view(), name='books_update'),
        path(r'<int:pk>/delete/', views.BookDelete.as_view(), name='books_delete'),
        ])
    ),

    path('author/', include([
        path('', views.AuthorListView.as_view(), name='authors-list'),
        path('<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

        path(r'create/', views.AuthorCreate.as_view(), name='author_create'),
        path(r'<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
        path(r'<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
        ])
    ),

    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.RenewBookLibrarian.as_view(), name='renew-book-librarian'),

]
