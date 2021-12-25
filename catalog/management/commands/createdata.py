from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import faker.providers
import faker.proxy
from faker import Faker

from catalog import models

import random
import datetime


class Provider(faker.providers.BaseProvider):

    def get_random_element_(self):
        return self.random_element([1, 2, 3, 4, 5])

    def get_due_back_for_book_instance(self, date_end_day):
        # generete some (datetime.now) + (31 days)
        now = datetime.datetime.now()
        some_days = datetime.timedelta(random.randint(1, date_end_day))
        in_some_days = now + some_days
        return Faker(['en']).date_between_dates(date_start=datetime.date.today(), date_end=in_some_days)

    def get_some_user_of_django(self):
        from django.contrib.auth.models import User
        return random.choice([val.id for val in User.objects.all()])


# ------------------------------------------------------------
class Command(BaseCommand):
    help = "Comand information"

    def __init__(self):
        super().__init__()
        self.fake = Faker(['en'])
        # self.fake.add_provider(Provider)

    def handle(self, *args, **options):
        self.fake.add_provider(Provider)

        self.generate_language()
        self.generate_genre()
        self.generate_author()
        # self.generate_book()
        # self.generate_book_instance()

    def generate_language(self):
        # iter all language
        language_ = ["en", "ru", "uk", ]

        if models.Language.objects.all().count() == 0:
            for val in iter(language_):
                models.Language.objects.create(name=val)
            else:
                check_genre = models.Language.objects.all().count()
                self.stdout.write(self.style.SUCCESS(f'Generate of Language`s {check_genre}'))

    def generate_genre(self):
        # iter all genre_for_books len 24
        genre_ = [
            # List of fiction book genres:
            'Adventure',
            'Fantasy',
            'Romance',
            'Contemporary',
            'Dystopian',
            'Mystery',
            'Horror',
            'Thriller',
            'Paranormal',
            'Historical fiction',
            'Science Fiction',
            'Children’s',
            # List of nonfiction book genres:
            'Memoir',
            'Cooking',
            'Art',
            'Self-help / Personal',
            'Development',
            'Motivational',
            'Health',
            'History',
            'Travel',
            'Guide / How-to',
            'Families & Relationships',
            'Humor',
        ]
        if models.Genre.objects.count() == 0:
            for val in iter(genre_):
                models.Genre.objects.create(name=val)
            else:
                check_genre = models.Genre.objects.all().count()
                self.stdout.write(self.style.SUCCESS(f'Generate of Genre`s {check_genre}'))

    def generate_author(self):
        if models.Author.objects.count() == 0:
            for _ in range(8):
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                date_of_birth = self.fake.date_of_birth()
                date_of_death = random.choice([None, self.fake.get_due_back_for_book_instance(date_end_day=32)])

                models.Author.objects.create(
                    first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, date_of_death=date_of_death
                )
            else:
                check_author = models.Author.objects.all().count()
                self.stdout.write(self.style.SUCCESS(f'Generate of Author {check_author}'))

    def generate_book(self):
        if models.Book.objects.count() == 0:
            for _ in range(15):
                title = self.fake.text(max_nb_chars=200)

                get_all_id_author = [val.id for val in models.Author.objects.all()]
                author_id = models.Author(id=random.choice(get_all_id_author))

                summary = self.fake.text(max_nb_chars=1000)
                imprint = self.fake.text(max_nb_chars=120)
                isbn = ''.join(self.fake.isbn13().split('-'))

                get_all_id_genre = [val.id for val in models.Author.objects.all()]
                genre_id = models.Genre(id=random.choice(get_all_id_genre))

                get_all_id_language = [val.id for val in models.Language.objects.all()]
                language_id = models.Language(id=random.choice(get_all_id_language))

                models.Book.objects.create(
                    title=title, author=author_id, summary=summary, imprint=imprint, isbn=isbn,
                    genre=genre_id, language=language_id
                )
            else:
                check_book = models.Book.objects.all().count()
                self.stdout.write(self.style.SUCCESS(f'Generate of Books {check_book}'))

    def generate_book_instance(self):
        if models.BookInstance.objects.count() == 0:
            for _ in range(20):
                get_all_id_book = [val.id for val in models.Book.objects.all()]
                book_id = random.choice(get_all_id_book)
                imprint = self.fake.text(max_nb_chars=200)

                due_back = self.fake.get_due_back_for_book_instance(date_end_day=32)

                borrower = self.fake.get_some_user_of_django()

                status = random.choice([val[0] for val in models.BookInstance.LOAN_STATUS])

                models.BookInstance.objects.create(
                    book=book_id, imprint=imprint, due_back=due_back, borrower=borrower, status=status,
                )
            else:
                check_book_instance = models.BookInstance.objects.all().count()
                self.stdout.write(self.style.SUCCESS(f'Generate of BookInstance {check_book_instance}'))
