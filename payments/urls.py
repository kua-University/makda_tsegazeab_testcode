from django.urls import path
from . import views

urlpatterns = [
    path('pay/', views.make_payment, name='make_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('get-course-price/<int:course_id>/', views.get_course_price, name='get_course_price'),
]



