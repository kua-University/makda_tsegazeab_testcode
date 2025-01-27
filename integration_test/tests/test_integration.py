from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from courses.models import Course
from registration.models import Registration
from payments.models import Payment
import stripe
from django.conf import settings


class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test users
        self.student = User.objects.create_user(username='student', password='password123', is_student=True)
        self.admin = User.objects.create_user(username='admin', password='password123', is_admin=True)
        # Create test course
        self.course = Course.objects.create(name='Django Basics', description='Learn Django', price=100.00)

    def test_user_registration_and_login(self):
        """Test registering a new student and logging in"""
        response = self.client.post(reverse('register'), {
            'username': 'newstudent',
            'password1': 'password123',
            'password2': 'password123',
            'is_student': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

        response = self.client.post(reverse('login'), {
            'username': 'newstudent',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_course_list_view(self):
        """Test retrieving the list of available courses"""
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.name)

class PaymentIntegrationTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student', password='studentpass', email='student@example.com',
                                                is_student=True)
        self.course = Course.objects.create(name='Test Course', description='Course Description', credit_hour=3,
                                            price=100.00)
        stripe.api_key = settings.STRIPE_SECRET_KEY # Use a test key

    def test_student_can_make_payment(self):
        self.client.login(username='student', password='studentpass')

        # Register for the course
        self.client.post(reverse('course_register', args=[self.course.id]), {})

        # Simulate making a payment
        response = self.client.post(reverse('make_payment'), {
            'course': self.course.id,
        })

        self.assertEqual(response.status_code, 302)  # Check for redirect after payment
        self.assertTrue(Payment.objects.filter(registration__student=self.student).exists())

class PaymentFailureTests(TestCase):
    def test_payment_failure_redirects(self):
        # Simulate a payment failure scenario
        response = self.client.get(reverse('payment_failed'))
        self.assertEqual(response.status_code, 200)  # Check that the failure page loads successfully



class UserLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', is_student=True)

    def test_user_can_logout(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)


class CoursePriceApiTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='Test Course', description='Course Description', price=100.00)

    def test_get_course_price(self):
        response = self.client.get(reverse('get_course_price', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'price': '100.00'})  # Check price returned correctly