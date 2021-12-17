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
        'catalog/index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )

# ________________________________________________________________________


from django.views import generic


class BookListView(generic.ListView):
    model = models.Book
    # paginate_by = 4
    template_name = 'catalog/book_list.html'


class BookDetailView(generic.DetailView):
    model = models.Book
    # queryset = model.objects.all().filter(id=pk)


class AuthorListView(generic.ListView):
    model = models.Author
    template_name = 'catalog/author_list.html'


class AuthorDetailView(generic.DetailView):
    model = models.Author


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

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(models.BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


# ________________________________________________________________________


from django.views.generic import edit
from django.urls import reverse_lazy


class AuthorCreate(PermissionRequiredMixin, edit.CreateView):
    model = models.Author
    fields = '__all__'
    initial = {'date_of_death': '01/01/2021', }
    permission_required = 'catalog.add_author'


class AuthorUpdate(PermissionRequiredMixin, edit.UpdateView):
    model = models.Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.change_author'


class AuthorDelete(PermissionRequiredMixin, edit.DeleteView):
    model = models.Author
    success_url = reverse_lazy('authors')
