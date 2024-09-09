from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .dependencies import Project


class UserListGenericViewTest(APITestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        User.objects.create(username="user1", first_name="John", last_name="Doe", email="john.doe@example.com")
        User.objects.create(username="user2", first_name="Jane", last_name="Smith", email="jane.smith@example.com")

    def test_get_user_list(self):
        # Делаем запрос к эндпоинту
        url = reverse('user-list')
        response = self.client.get(url)

        # Проверяем, что запрос успешен
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем количество пользователей
        self.assertEqual(len(response.data), 2)


class RegisterUserGenericViewTest(APITestCase):
    def test_register_new_user(self):
        url = reverse('user-register')
        data = {
            "username": "new_user",
            "first_name": "New",
            "last_name": "User",
            "email": "new.user@example.com",
            "password": "strong_password",
            "re_password": "strong_password",
            "position": "Programmer"
        }
        response = self.client.post(url, data, format='json')

        # Проверка успешной регистрации
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'new_user')

    def test_invalid_username(self):
        """Тестируем, что username не может содержать недопустимые символы"""
        data = {
            "username": "invalid@username!",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": "Programmer",
            "password": "validpassword123",
            "re_password": "validpassword123"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Username must contain only letters, numbers, or _')

    def test_invalid_first_name(self):
        """Тестируем, что имя не должно содержать цифры или специальные символы"""
        data = {
            "username": "validusername",
            "first_name": "John123",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": "Programmer",
            "password": "validpassword123",
            "re_password": "validpassword123"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'First name must contain only letters')

    def test_invalid_email(self):
        """Тестируем, что неверные email-адреса отклоняются"""
        data = {
            "username": "validusername",
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "position": "Programmer",
            "password": "validpassword123",
            "re_password": "validpassword123"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(str(response.data['email'][0]), 'Enter a valid email address.')

    def test_password_mismatch(self):
        """Тестируем, что пароли должны совпадать"""
        data = {
            "username": "validusername",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": "Programmer",
            "password": "validpassword123",
            "re_password": "differentpassword123"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(str(response.data['password'][0]), 'Passwords do not match')

    def test_short_password(self):
        """Тестируем, что короткие пароли отклоняются"""
        data = {
            "username": "validusername",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": "Programmer",
            "password": "short",
            "re_password": "short"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]),
                         'This password is too short. It must contain at least 8 characters.')

    def test_unique_email(self):
        """Тестируем, что email должен быть уникальным"""
        User.objects.create(username="existinguser", first_name="John", last_name="Doe", email="john.doe@example.com",
                            password="validpassword123")

        data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "john.doe@example.com",
            "password": "validpassword123",
            "re_password": "validpassword123",
            "position": "Programmer"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(str(response.data['email'][0]), 'user with this email address already exists.')

    def test_missing_re_password(self):
        """Тестируем, что re_password должен быть передан"""
        data = {
            "username": "validusername",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "validpassword123",
            "position": "Programmer"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('re_password', response.data)

    def test_missing_username(self):
        """Тестируем, что отсутствие username вызывает ошибку"""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": "Programmer",
            "password": "validpassword123",
            "re_password": "validpassword123"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_invalid_position(self):
        """Тестируем, что неверное значение position вызывает ошибку"""
        data = {
            "username": "validusername",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": "InvalidPosition",
            "password": "validpassword123",
            "re_password": "validpassword123"
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('position', response.data)
        self.assertEqual(str(response.data['position'][0]), '"InvalidPosition" is not a valid choice.')


class UserRetrieveTest(APITestCase):
    def setUp(self):
        # Создаем проект для пользователя
        self.project = Project.objects.create(name="AgileProject")
        # Создаем тестового пользователя
        self.user = User.objects.create(
            username="user1",
            first_name="John",
            last_name="Doe",
            email="user1@example.com",
            phone="+123456789",
            position="Developer",
            project=self.project
        )

    def test_get_user_by_id(self):
        """Тестируем получение информации о пользователе по ID"""
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)

        # Проверяем, что запрос успешен
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем данные в ответе
        self.assertEqual(response.data['username'], 'user1')
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'user1@example.com')
        self.assertEqual(response.data['phone'], '+123456789')
        self.assertEqual(response.data['position'], 'Developer')
        self.assertEqual(response.data['project'], 'AgileProject')

    def test_get_nonexistent_user(self):
        """Тестируем получение информации о несуществующем пользователе"""
        url = reverse('user-detail', args=[999])  # Несуществующий ID
        response = self.client.get(url)

        # Проверяем, что запрос вернет 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User not found')
