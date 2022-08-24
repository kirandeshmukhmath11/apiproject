from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#
# Create your views here.

class HealthCheckView(APIView):
    # Swagger Descriptions start here
    OPERATIONSDESCRIPTION = """ 
        This is the health Check API and required no input
        """
    PROPERTIESDESCRIPTION = {
    }
    REQUIREDLIST = []
    RESPONSEDESCRIPTION = '''

        | Key Name                      | Description                                             |
        | ------------------------------| --------------------------------------------------------|
        | message                       | Will return true if API is called, else will throw error |

        '''

    ################# Swagger Descriptions start here  #####################

    @swagger_auto_schema(
        responses={200: RESPONSEDESCRIPTION})
    def get(self, request):
        output_json = {"message": True}
        return Response(output_json, status=status.HTTP_200_OK)

