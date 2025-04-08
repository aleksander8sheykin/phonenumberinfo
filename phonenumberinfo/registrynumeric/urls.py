from django.urls import re_path

from registrynumeric.views import PhonenumberDetail

urlpatterns = [
    re_path('registrynumeric/(?P<phonenumber>[0-9]{11})/', PhonenumberDetail.as_view(), name='phonenumber-detail'),
]
