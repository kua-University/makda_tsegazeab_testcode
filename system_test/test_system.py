from django.test import LiveServerTestCase
from django.urls import reverse
from users.models import User
from courses.models import Course
from payments.models import Payment

class UserRegistrationAutomationTest(LiveServerTestCase):
    def test_user_can_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'StrongPassword!123',
            'password2': 'StrongPassword!123',
            'email': 'testuser@example.com',
            'age': 20,  # Include age
            'is_student': True,
        })

        # Check for redirect status code
        if response.status_code == 302:
            user_exists = User.objects.filter(username='testuser').exists()
            self.assertTrue(user_exists)
        else:
            print("Form submission failed with errors:")
            print(response.content.decode())
            self.assertEqual(response.status_code, 302)


class UserLoginAutomationTest(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='StrongPassword!123', is_student=True)

    def test_user_can_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPassword!123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login


class CourseCreationAutomationTest(LiveServerTestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True)

    def test_admin_can_create_course(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('add_course'), {
            'name': 'Automated Course',
            'description': 'Automated Course Description',
            'credit_hour': 3,
            'price': 150.00,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(name='Automated Course').exists())

class PaymentSuccessPageAutomationTest(LiveServerTestCase):
    def test_access_payment_success_page(self):
        response = self.client.get(reverse('payment_success'))
        self.assertEqual(response.status_code, 200)  # Should load success page

class PaymentFailurePageAutomationTest(LiveServerTestCase):
    def test_access_payment_failure_page(self):
        response = self.client.get(reverse('payment_failed'))
        self.assertEqual(response.status_code, 200)  # Should load failure page