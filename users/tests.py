from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import User

class UserViewTests(TestCase):

    def setUp(self):
        # Create a test client
        self.client = Client()

        # Define URLs
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com',
            age=25,
            is_student=True
        )

    def test_register_view_get(self):
        """Test GET request to the register view"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post_valid(self):
        """Test POST request to the register view with valid data"""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'age': 20,
            'is_student': True,
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        """Test POST request to the register view with invalid data"""
        response = self.client.post(self.register_url, {
            'username': '',  # Invalid username
            'email': 'invalidemail',  # Invalid email
            'age': 'invalidage',  # Invalid age
            'password1': 'password',
            'password2': 'password123',  # Passwords don't match
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, 'This field is required.', html=True)
        self.assertContains(response, 'Enter a valid email address.', html=True)
        self.assertContains(response, 'Enter a whole number.', html=True)
        self.assertContains(response, 'The two password fields didn’t match.', html=True)

    def test_login_view_get(self):
        """Test GET request to the login view"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_valid(self):
        """Test POST request to the login view with valid credentials"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to course_list
        self.assertRedirects(response, reverse('course_list'))

    def test_login_view_post_invalid(self):
        """Test POST request to the login view with invalid credentials"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_logout_view(self):
        """Test the logout view"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, self.login_url)
