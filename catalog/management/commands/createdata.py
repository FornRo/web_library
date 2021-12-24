import random

import faker.providers
import faker.proxy
from django.core.management.base import BaseCommand
from faker import Faker
from catalog import models
import json
import datetime


class Provider(faker.providers.BaseProvider):

    def get_random_element_(self):
        return self.random_element([1, 2, 3, 4, 5])



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
        for val in iter(language_):
            models.Language.objects.create(name=val)
        else:
            check_genre = models.Language.objects.all().count()
            self.stdout.write(self.style.SUCCESS(f'Number of Language {check_genre}'))

    def generate_genre(self):
        check_genre = models.Genre.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f'Number of genre {check_genre}'))

        # iter all genre_for_books
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
        for val in iter(genre_):
            models.Genre.objects.create(name=val)
        else:
            check_genre = models.Genre.objects.all().count()
            self.stdout.write(self.style.SUCCESS(f'Number of Genre {check_genre}'))
