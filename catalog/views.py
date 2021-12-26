from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = models.Book.objects.all().count()
    num_instances = models.BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available = models.BookInstance.objects.filter(status__exact='a').count()
    num_authors = models.Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


# ________________________________________________________________________
from django.views import generic


class BookListView(generic.ListView):
    model = models.Book
    paginate_by = 4
    template_name = 'catalog/book_list.html'


class BookDetailView(generic.DetailView):
    model = models.Book
    # queryset = model.objects.all().filter(id=pk)


class AuthorListView(generic.ListView):
    model = models.Author
    template_name = 'catalog/author_list.html'


class AuthorDetailView(generic.DetailView):
    model = models.Author


# ________________________________________________________________________
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksByUserListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = models.BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# ________________________________________________________________________
from django.views.generic import edit
from . import forms
from django.urls import reverse


class RenewBookLibrarian(PermissionRequiredMixin, edit.UpdateView):
    form_class = forms.RenewBookModelForm
    initial = {'key': 'value'}
    template_name = r'catalog\book_renew_librarian.html'

    def get(self, request):
        form = self.form_class(self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return reverse('all-borrowed')

        return render(request, self.template_name, {'form': form})


# ________________________________________________________________________


from django.urls import reverse_lazy


class AuthorCreate(PermissionRequiredMixin, edit.CreateView):
    model = models.Author
    fields = '__all__'
    initial = {'date_of_death': '', }
    permission_required = 'catalog.add_author'


class AuthorUpdate(PermissionRequiredMixin, edit.UpdateView):
    model = models.Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.change_author'


class AuthorDelete(PermissionRequiredMixin, edit.DeleteView):
    model = models.Author
    success_url = reverse_lazy('catalog:authors-list')
    permission_required = 'catalog.delete_author'


class BookCreate(PermissionRequiredMixin, edit.CreateView):
    model = models.Book
    fields = '__all__'
    initial = {
        'summary': 'summary === Lorem ipsum dolor sit amet.',
        'imprint': 'imprint === Lorem ipsum dolor sit amet.',
        'language': 'eng',
    }
    permission_required = 'catalog.add_book'


class BookUpdate(PermissionRequiredMixin, edit.UpdateView):
    model = models.Book
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.change_book'


class BookDelete(PermissionRequiredMixin, edit.DeleteView):
    model = models.Book
    success_url = reverse_lazy('catalog:books-list')
    permission_required = 'catalog.delete_book'

