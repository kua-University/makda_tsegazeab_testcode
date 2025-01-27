from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.

# tests/test_models.py
from django.test import TestCase
from .models import Registration
from users.models import User
from courses.models import Course
from .forms import RegistrationForm
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import register_for_course

class RegistrationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student1', password='testpass', is_student=True)
        self.course = Course.objects.create(name='Mathematics', description='Math course', credit_hour=3, price=150.00)
        self.registration = Registration.objects.create(student=self.user, course=self.course)

    def test_registration_str(self):
        self.assertEqual(str(self.registration), 'student1 registered for Mathematics')

# tests/test_views.py
class RegistrationViewsTest(TestCase):
    def setUp(self):
        # Create a test user and course
        self.user = User.objects.create_user(username='student1', password='testpass', is_student=True)
        self.course = Course.objects.create(name='Mathematics', description='Math course', credit_hour=3, price=150.00)
        self.client.login(username='student1', password='testpass')

    def test_register_for_course_view_success(self):
        # Test successful registration
        response = self.client.post(reverse('course_register', args=[self.course.id]), {
            'course': self.course.id  # Assuming 'course' is the field in your RegistrationForm
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertTrue(Registration.objects.filter(student=self.user, course=self.course).exists())

    def test_register_for_course_view_invalid(self):
        # Test registration with invalid data
        response = self.client.post(reverse('course_register', args=[self.course.id]), {
            'course': ''  # Simulate invalid input
        })
        print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, 200)  # Should return to the same page
        self.assertFalse(Registration.objects.filter(student=self.user, course=self.course).exists())

    def test_register_for_nonexistent_course(self):
        # Test registration for a nonexistent course
        response = self.client.post(reverse('course_register', args=[999]), {  # Assuming 999 does not exist
            'course': self.course.id  # Any valid course ID for the post data
        })
        self.assertEqual(response.status_code, 404)  # Should return a 404 error

# tests/test_urls.py



class RegistrationUrlsTest(SimpleTestCase):
    def test_register_for_course_url(self):
        url = reverse('course_register', args=[1])  # Use a sample course_id
        self.assertEqual(resolve(url).func, register_for_course)