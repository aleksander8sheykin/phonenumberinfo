from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from registrynumeric.models import Range
from registrynumeric.serializers import PhonenumberInfo


class PhonenumberDetail(APIView):

    def get(self, request, *args, **kwargs) -> Response:
        prefix = int(kwargs.get('phonenumber')[1:4])
        number = int(kwargs.get('phonenumber')[4:])
        try:
            range_one = Range.objects.get(prefix=prefix, number_from__lte=number, number_to__gte=number)
        except Range.DoesNotExist:
            raise Http404

        return Response(PhonenumberInfo(range_one).data)
