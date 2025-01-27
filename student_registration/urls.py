
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Import redirect


urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('registration/', include('registration.urls')),
    path('payments/', include('payments.urls')),
]
    