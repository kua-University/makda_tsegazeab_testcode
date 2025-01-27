from django.test import TestCase

# Create your tests here.
# tests/test_models.py
from django.test import TestCase
from .models import Course
from django.urls import reverse, resolve
from .views import add_course, course_list
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Mathematics',
            description='Basic Math Course',
            credit_hour=3,
            price=150.00
        )

    def test_course_str(self):
        self.assertEqual(str(self.course), 'Mathematics')

    def test_course_fields(self):
        self.assertEqual(self.course.credit_hour, 3)
        self.assertEqual(self.course.price, 150.00)

# tests/test_views.py

User = get_user_model()

class CourseViewsTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True)
        self.client.login(username='admin', password='adminpass')

    def test_add_course_view(self):
        response = self.client.post(reverse('add_course'), {
            'name': 'Physics',
            'description': 'Basic Physics Course',
            'credit_hour': 4,
            'price': 200.00
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(name='Physics').exists())

    def test_course_list_view(self):
        Course.objects.create(name='Chemistry', description='Basic Chemistry Course', credit_hour=3, price=180.00)
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chemistry')

    # tests/test_urls.py


class CourseUrlsTest(SimpleTestCase):
    def test_add_course_url(self):
        url = reverse('add_course')
        self.assertEqual(resolve(url).func, add_course)

    def test_course_list_url(self):
        url = reverse('course_list')
        self.assertEqual(resolve(url).func, course_list)