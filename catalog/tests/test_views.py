import datetime
from unittest import TestCase

from django.urls import reverse
from django.utils import timezone

from .. import models
from django.contrib.auth.models import User  # Необходимо для представления User как borrower


class LoanedBookInstancesByUserListViewTest(TestCase):

    def setUp(self):
        # Создание двух пользователей
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        # Создание книги
        test_author = models.Author.objects.create(first_name='John', last_name='Smith')
        test_genre = models.Genre.objects.create(name='Fantasy')
        test_language = models.Language.objects.create(name='English')
        test_book = models.Book.objects.create(title='Book Title', summary = 'My book summary', isbn='ABCDEFG', author=test_author, language=test_language)
        # Create genre as a post-step
        genre_objects_for_book = models.Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Присвоение типов many-to-many напрямую недопустимо
        test_book.save()

        # Создание 30 объектов BookInstance
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date= timezone.now() + datetime.timedelta(days=book_copy%5)
            if book_copy % 2:
                the_borrower=test_user1
            else:
                the_borrower=test_user2
            status='m'
            models.BookInstance.objects.create(book=test_book,imprint='Unlikely Imprint, 2016', due_back=return_date, borrower=the_borrower, status=status)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'catalog/bookinstance_list_borrowed_user.html')


from django.contrib.auth.models import Permission  # Required to grant the permission needed to set a book as returned.


class RenewBookInstancesViewTest(TestCase):

    def setUp(self):
        # Создание пользователя
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Создание книги
        test_author = models.Author.objects.create(first_name='John', last_name='Smith')
        test_genre = models.Genre.objects.create(name='Fantasy')
        test_language = models.Language.objects.create(name='English')
        test_book = models.Book.objects.create(title='Book Title', summary = 'My book summary', isbn='ABCDEFG',
                                               author=test_author, language=test_language,)
        # Создание жанра Create genre as a post-step
        genre_objects_for_book = models.Genre.objects.all()
        test_book.genre=genre_objects_for_book
        test_book.save()

        # Создание объекта BookInstance для для пользователя test_user1
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = models.BookInstance.objects.create(book=test_book,imprint='Unlikely Imprint, 2016',
                                                                     due_back=return_date, borrower=test_user1,
                                                                     status='o')

        # Создание объекта BookInstance для для пользователя test_user2
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = models.BookInstance.objects.create(book=test_book, imprint='Unlikely Imprint, 2016',
                                                                     due_back=return_date, borrower=test_user2,
                                                                     status='o')
