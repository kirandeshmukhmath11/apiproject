from rest_framework.response import Response
from rest_framework.views import APIView

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#
from utilities.credmanager.credentials.aws_secrets_authentication import aws_secrets_authentication
import http.client
import json

import logging

logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')


# @permission_classes([AllowAny])
class GetPapertrailLogs(APIView):
    # Swagger Descriptions start here
    OPERATIONSDESCRIPTION = """ 
    This function will fetch Papertrail logs
    All parameters are optional.

    refer https://www.papertrail.com/help/search-api/ for complete details on input parameters, their properties 
    and definitions, and output.
    Note Timestamps for min_time and max_time should be in epoch time UTC.
    """
    PROPERTIESDESCRIPTION = {
        'q': openapi.Schema(type=openapi.TYPE_STRING,
                                       description='search query; return events matching this query '
                                                   '(default: return all events)', example='%27Critical%20error%27'),
        'system_id': openapi.Schema(type=openapi.TYPE_STRING,
                               description='limit results to a specific system (accepts ID or name)', example='11571567131'),
        'group_id': openapi.Schema(type=openapi.TYPE_STRING,
                                         description='limit results to a specific group (accepts ID only)', example='2345'),
        'min_id': openapi.Schema(type=openapi.TYPE_STRING,
                               description='the oldest message ID to examine', example='7711561783320576'),
        'max_id': openapi.Schema(type=openapi.TYPE_STRING,
                                         description='the newest message ID to examine', example='7711582041804800'),
        'min_time': openapi.Schema(type=openapi.TYPE_STRING,
                               description='the oldest timestamp to examine. Should be in epoch time UTC', example='1658040822'),
        'max_time': openapi.Schema(type=openapi.TYPE_STRING,
                                         description='the newest timestamp to examine. Should be in epoch time UTC', example='1656658422'),
        'limit': openapi.Schema(type=openapi.TYPE_STRING,
                               description='maximum messages to return (default 1000, maximum 10,000)', example='6'),
        'tail': openapi.Schema(type=openapi.TYPE_STRING,
                                         description='search approach to use. takes values of true or false', example='false')

    }
    REQUIREDLIST = []
    RESPONSEDESCRIPTION = '''
    refer https://www.papertrail.com/help/search-api/ for complete details on input parameters, their properties 
    and definitions, and output
    '''

    ################# Swagger Descriptions start here  #####################

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,

        required=REQUIREDLIST,
        properties=PROPERTIESDESCRIPTION),
        operation_description=OPERATIONSDESCRIPTION,
        responses={200: RESPONSEDESCRIPTION})
    @aws_secrets_authentication
    def post(self, request):
        """
        :param request:
        :return:
        """
        logger_info.info("get_papertrail_logs Post function called")
        input_json=request.data
        conn = http.client.HTTPSConnection(host='papertrailapp.com')
        papertrail_base_url = '/api/v1/events/search.json'
        customized_url = papertrail_base_url
        import pdb; pdb.set_trace()
        for item in input_json.keys():
            if customized_url == papertrail_base_url:
                customized_url = f"{customized_url}?{item}={input_json[item]}"
            else:
                customized_url = f"{customized_url}&{item}={input_json[item]}"
        conn.request(
            method='GET',
            url='/api/v1/events/search.json',
            headers={'X-Papertrail-Token': 'Hh9In2SxaPytEDHivXg'})
        response = conn.getresponse()
        output_json = json.loads(response.read())
        return Response(output_json)
