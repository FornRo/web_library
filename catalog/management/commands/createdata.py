import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker
from catalog import models
import json

LANGUAGE = ["en", "ru", "uk", ]


class Provider(faker.providers.BaseProvider):
    def generate_genre(self):
        return self.



class Command(BaseCommand):
    help = "Comand information"

    def handle(self, *args, **options):
        fake = Faker(['en'])
        fake.add_provider(Provider)
        # iter all language
        for val in iter(LANGUAGE):
            models.Language.objects.create(name=val)
        else:
            check_genre = models.Genre.objects.all().count()
            self.stdout.write(self.style.SUCCESS(f'Number of genre {check_genre}'))
        # print(fake.name())
