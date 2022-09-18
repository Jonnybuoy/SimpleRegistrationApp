from django.urls import path

from .views import *

urlpatterns = [
    path('register/', user_registration, name='register'),
    path('update_record/<int:id>/', update_record, name='update_record'),
    path('registrationapi', RegistrationDetailsAPIView.as_view()),
    path('registration_report', UserRegistrationReport.as_view(), name='registration_report')
]