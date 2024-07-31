import requests
from django.conf import settings
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class GetData(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        api_endpoint = f"{settings.BASE_URL}/national_assembly/members/"

        try:
            response = requests.get(api_endpoint, verify=False)
            response.raise_for_status()

            data = response.json()

            return Response(data, status=response.status_code)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=500)