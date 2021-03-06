from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from unittest import skip

from django.utils import timezone
import datetime
import pytz

from .models import Book, BookStatus
from .serializers import BookStatusSerializer

from django.apps import apps
User = apps.get_model('userauth','User')

class PostBookStatusTest(APITestCase):
    # given a book id and bookstatus data (code, datetime), 
    # should make a new bookstatus row and return its data

    def setUp(self):
        self.user = User.objects.create(
            username='Bertie', password='password')
        self.token = str(self.user.auth_token)

        iso_date = pytz.utc.localize(datetime.datetime(2020, 1, 1)).isoformat()
        self.book = Book.objects.create(
            title="Post Status Test", 
            user=self.user,
            current_status=Book.WANTTOREAD, 
            current_status_date=iso_date)

    def test_can_create_a_valid_bookstatus(self):
        status_code = Book.PAUSED
        date = pytz.utc.localize(datetime.datetime(2020, 1, 16)).isoformat()#.strftime("%Y-%m-%dT%H:%M:%SZ")

        data = {
            "status_code": status_code,
            "date": date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': self.book.id})
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['status']['status_code'], status_code)
        self.assertEqual(response.data['status']['book'], self.book.id)
        self.assertEqual(response.data['status']['date'], date)

        filtered_statuses = BookStatus.objects.filter(
            user=self.user, book=self.book, status_code=status_code)
        self.assertTrue(filtered_statuses.exists())

    def test_adding_a_bookstatus_changes_books_current_status(self):
        status_code = Book.COMPLETED
        date = pytz.utc.localize(datetime.datetime(2021, 1, 16))
        iso_date = date.isoformat()

        data = {
            "status_code": status_code,
            "date": iso_date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': self.book.id})
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        filtered_statuses = BookStatus.objects.filter(
            user=self.user, book=self.book, status_code=status_code)
        self.assertTrue(filtered_statuses.exists())
        self.assertEqual(filtered_statuses[0].book, self.book)
        self.assertEqual(filtered_statuses[0].book.current_status, Book.COMPLETED)
        self.assertEqual(filtered_statuses[0].book.current_status_date, date)

    def test_adding_a_bookstatus_changes_books_current_status_date(self):
        status_code = Book.COMPLETED
        date = pytz.utc.localize(datetime.datetime(2020, 1, 18))
        iso_date = pytz.utc.localize(datetime.datetime(2020, 1, 18)).isoformat()

        data = {
            "status_code": status_code,
            "date": iso_date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': self.book.id})
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        filtered_statuses = BookStatus.objects.filter(
            user=self.user, book=self.book, status_code=status_code)
        self.assertTrue(filtered_statuses.exists())
        self.assertEqual(filtered_statuses[0].book, self.book)
        self.assertEqual(filtered_statuses[0].book.current_status_date, date)

    def test_adding_a_historical_bookstatus_does_not_change_books_current_status_date(self):
        current_date = pytz.utc.localize(datetime.datetime(2020, 1, 17))
        iso_current_date = pytz.utc.localize(datetime.datetime(2020, 1, 17)).isoformat()

        book = Book.objects.create(
            title="Post Historical Status Test", 
            user=self.user, 
            current_status=Book.COMPLETED,
            current_status_date=current_date
        )
        existing_status = BookStatus.objects.create(
            status_code=Book.COMPLETED,
            book=book,
            user=self.user,
            date=iso_current_date
        )

        status_code = Book.CURRENT
        prior_date = pytz.utc.localize(datetime.datetime(2020, 1, 2))
        iso_prior_date = pytz.utc.localize(datetime.datetime(2020, 1, 2)).isoformat()
        data = {
            "status_code": status_code,
            "date": iso_prior_date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': book.id})
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        filtered_statuses = BookStatus.objects.filter(
            user=self.user, book=book, status_code=status_code)
        self.assertTrue(filtered_statuses.exists())

        affected_book = Book.objects.get(id=book.id)
        self.assertEqual(affected_book.current_status, Book.COMPLETED)
        self.assertEqual(affected_book.current_status_date, current_date)

    def test_cannot_create_a_bookstatus_without_a_status(self):
        date = pytz.utc.localize(datetime.datetime(2020, 1, 16)).isoformat()
        data = {
            "date": date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': self.book.id})
        response = self.client.post(url, data, format='json')

        expected_data = {
            "error": "Invalid status parameters"
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_cannot_create_a_bookstatus_with_an_invalid_status(self):
        date = pytz.utc.localize(datetime.datetime(2020, 1, 16)).isoformat()
        data = {
            "status_code": "in progress",
            "date": date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': self.book.id})
        response = self.client.post(url, data, format='json')

        expected_data = {
            "error": "Invalid status code"
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_cannot_create_a_bookstatus_without_a_date(self):
        status_code = Book.PAUSED
        
        data = {
            "status_code": status_code,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': self.book.id})
        response = self.client.post(url, data, format='json')

        expected_data = {
            "error": "Invalid status parameters"
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_cannot_create_a_bookstatus_with_an_invalid_date(self):
        status_code = Book.PAUSED
        date = "Date"
        
        data = {
            "status_code": status_code,
            "date": date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': self.book.id})
        response = self.client.post(url, data, format='json')

        expected_data = {
            "error": ['“Date” value has an invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.']
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_returns_error_for_nonexisting_book(self):
        fake_id = 999
        status_code = Book.PAUSED
        date = pytz.utc.localize(datetime.datetime(2020, 1, 16))
        
        data = {
            "status_code": status_code,
            "date": date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': fake_id})
        response = self.client.post(url, data, format='json')

        expected_data = {
            "error": "Could not find book with ID: %s" %(fake_id)
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_returns_error_for_a_book_that_is_not_the_users(self):
        other_user = User.objects.create(
            username="other user", password="password")
        other_book = Book.objects.create(
            title="Get Status by User's Book Test", user=other_user)

        status_code = Book.PAUSED
        date = pytz.utc.localize(datetime.datetime(2020, 1, 16))
        data = {
            "status_code": status_code,
            "date": date
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('bookstatus', kwargs={'id': other_book.id})
        response = self.client.post(url, data, format='json')

        expected_data = {
            "error": "Could not find book with ID: %s" %(other_book.id)
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)
