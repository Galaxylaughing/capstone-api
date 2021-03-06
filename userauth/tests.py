from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from unittest import skip

# Create your tests here.
from .models import User
from .serializers import UserSerializer

from django.apps import apps
Book = apps.get_model('api', 'Book')


class UserTest(TestCase):
    """ Test module for User model """

    def setUp(self):
        """ create a user instance """
        self.user = User.objects.create(
          username='Caspar', password='acoolpassword')
        
        """ create serializer instance """
        self.serializer = UserSerializer(instance=self.user)
        self.serializer_keys = ['id', 'username']
    
    def test_user_is_created(self):
        """ assert setup user was added """
        self.assertEqual(User.objects.count(), 1)

        """ create new user """
        User.objects.create(
            username="Zanzibar", password='anothercoolpassword')

        """ assert count has changed """
        self.assertEqual(User.objects.count(), 2)
    
    def test_username_matches(self):
        user = self.user
        self.assertEqual(
            user.get_username(), 'Caspar')
    
    def test_hash_id_exists(self):
        user = self.user
        self.assertIsInstance(
          user.hash_id, str)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), self.serializer_keys)

    def test_serializer_returns_correct_username(self):
        data = self.serializer.data
        self.assertEqual(
            data['username'], self.user.get_username())

    def test_serializer_returns_a_hash(self):
        data = self.serializer.data
        self.assertIsInstance(
          data['id'], str)


class UserBookRelationshipTest(TestCase):

    def setUp(self):
        # create a user instance
        self.user = User.objects.create(
          username='Caspar', password='acoolpassword')

    def test_can_have_a_book(self):
        expectedCount = self.user.book_set.count() + 1

        book = Book.objects.create(
            title="Test Book", user=self.user)

        userBooks = self.user.book_set
        self.assertEqual(userBooks.count(), expectedCount)

        bookUser = book.user
        self.assertEqual(bookUser.username, self.user.username)

    def test_can_have_many_books(self):
        expectedCount = self.user.book_set.count() + 2

        Book.objects.create(
            title="Test Book", user=self.user)
        Book.objects.create(
            title="Other Test Book", user=self.user)

        userBooks = self.user.book_set
        self.assertEqual(userBooks.count(), expectedCount)


@skip("unused; using obtain_auth_token to login")
class LoginUserTest(APITestCase):
    """ Test module for logging in a User """

    def setUp(self):
        """ create a user instance to login """
        self.user = User.objects.create_user(
            username='Caspar', password='acoolpassword')

    def test_can_login_existing_user(self):
        # get API response
        url = reverse('login')
        data = {'username': 'Caspar', 'password': 'acoolpassword'}
        response = self.client.post(url, data, format='json')

        # get data from database
        user = User.objects.get(username='Caspar')
        serializer = UserSerializer(user)

        # assert
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_login_new_user(self):
        # get API response
        url = reverse('login')
        data = {'username': 'Newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Account not found')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SignUpUserTest(APITestCase):
    """ Test module for signing up a new User """

    def test_cannot_sign_up_existing_user(self):
        # create user
        User.objects.create_user(
            username='Caspar', password='acoolpassword')

        # get API response
        url = reverse('signup')
        data = {'username': 'Caspar', 'password': 'acoolpassword'}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Account already exists')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_sign_up_new_user(self):
        # get API response
        url = reverse('signup')
        data = {'username': 'Ducky', 'password': 'verysecurepassword'}
        response = self.client.post(url, data, format='json')

        # get data from database
        user = User.objects.get(username='Ducky')
        serializer = UserSerializer(user)

        # assert
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_sign_up_user_without_username(self):
        # get API response
        url = reverse('signup')
        data = {'password': 'acoolpassword'}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Error: username is missing or empty')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_sign_up_user_with_empty_username(self):
        # get API response
        url = reverse('signup')
        data = {'username': '', 'password': 'acoolpassword'}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Error: username is missing or empty')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cannot_sign_up_user_without_password(self):
        # get API response
        url = reverse('signup')
        data = {'username': 'Ducky'}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Error: password is missing or empty')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_sign_up_user_with_empty_password(self):
        # get API response
        url = reverse('signup')
        data = {'username': 'Ducky', 'password': ''}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Error: password is missing or empty')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_sign_up_without_username_or_password(self):
        # get API response
        url = reverse('signup')
        data = {}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Errors: username is missing or empty, password is missing or empty')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_sign_up_with_empty_username_and_password(self):
        # get API response
        url = reverse('signup')
        data = {'username': '', 'password': ''}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.data, 'Errors: username is missing or empty, password is missing or empty')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@skip("unused; using Token Authentication")
class LogoutUserTest(APITestCase):
    """ Test module for logging out a User """

    def setUp(self):
        # create a new user
        username = 'Logout Test'
        password = 'password'
        self.user = User.objects.create(
            username=username, password=password)
        
        # get user's token
        self.token = str(self.user.auth_token)

    def test_can_logout_an_authenticated_user(self):
        # add token to header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # get API response
        url = reverse('logout')
        response = self.client.get(url, format='json')

        # # assert
        self.assertEqual(response.data, 'Successfully logged out')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_logout_unauthenticated_user(self):
        # don't add token to header        
        # get API response
        url = reverse('logout')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
