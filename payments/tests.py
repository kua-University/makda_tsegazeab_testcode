from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
# tests/test_models.py

from django.test import TestCase
from users.models import User
from courses.models import Course
from registration.models import Registration
from .models import Payment
from django.test import TestCase
from .forms import PaymentForm
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import make_payment, payment_success, payment_failed, get_course_price

#test models.py
class PaymentModelTest(TestCase):
    def setUp(self):
        # Create a user, course, and registration for the test
        self.user = User.objects.create_user(username='student1', password='testpass', is_student=True)
        self.course = Course.objects.create(name='Mathematics', description='Math course', price=150.00, credit_hour=10)
        self.registration = Registration.objects.create(student=self.user, course=self.course)
        self.payment = Payment.objects.create(registration=self.registration, amount=150.00)

    def test_payment_str(self):
        expected_str = f'Payment for {self.user.username} - {self.payment.amount} (Pending)'
        self.assertEqual(str(self.payment), expected_str)


# tests/test_views.py



class PaymentViewsTest(TestCase):
    def setUp(self):
        # self.user = User.objects.create_user(username='student1', password='testpass', is_student=True)
        self.user = User.objects.create_user(
            username='student1',
            password='testpass',
            email='makdatsegazeab93@gmail.com',  # Ensure valid email
            is_student=True
        )
        self.client.login(username='student1', password='testpass')

        self.course = Course.objects.create(name='Mathematics', description='Math course', price=150.00, credit_hour=10)
        self.registration = Registration.objects.create(student=self.user, course=self.course)

    def test_make_payment_view(self):
        response = self.client.post(reverse('make_payment'), {
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect to Stripe checkout
        self.assertTrue(Payment.objects.filter(registration=self.registration).exists())
        payment = Payment.objects.get(registration=self.registration)
        self.assertEqual(payment.amount, self.course.price)
        self.assertEqual(payment.status, 'Pending')

    def test_payment_success_view(self):
        response = self.client.get(reverse('payment_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment_success.html')

    def test_payment_failed_view(self):
        response = self.client.get(reverse('payment_failed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment_failed.html')

    def test_get_course_price_view(self):
        response = self.client.get(reverse('get_course_price', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)

        # Convert the price to a float and compare
        expected_price = float(self.course.price)
        response_price = float(response.json()['price'])  # Get the price from the response
        self.assertEqual(response_price, expected_price)

    def test_get_course_price_invalid_course(self):
        response = self.client.get(reverse('get_course_price', args=[999]))  # Assuming 999 does not exist
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error': 'Course not found'})

# tests/test_urls.py
class PaymentURLsTest(SimpleTestCase):
    def test_make_payment_url(self):
        url = reverse('make_payment')
        self.assertEqual(url, '/payments/pay/')
        self.assertEqual(resolve(url).func, make_payment)

    def test_payment_success_url(self):
        url = reverse('payment_success')
        self.assertEqual(url, '/payments/success/')
        self.assertEqual(resolve(url).func, payment_success)

    def test_payment_failed_url(self):
        url = reverse('payment_failed')
        self.assertEqual(url, '/payments/failed/')
        self.assertEqual(resolve(url).func, payment_failed)

    def test_get_course_price_url(self):
        url = reverse('get_course_price', args=[1])
        self.assertEqual(url, '/payments/get-course-price/1/')
        self.assertEqual(resolve(url).func, get_course_price)
