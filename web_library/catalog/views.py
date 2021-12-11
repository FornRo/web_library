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


class AuthorDetailView(generic.DetailView):
    model = models.Author

