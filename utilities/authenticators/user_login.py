# from requests import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from utilities.credmanager.credentials.get_credentials import get_cred


@permission_classes([AllowAny])
class UserLogin(APIView):
    """
    This API is used to signin  the caller using keys provided to them
    """
    def post(self, request):
        """
        This function logs in the user using keys provided to them
        :param request:
        :return:
        """
        try:

            # input_json = request.data
            # # input_json = request.POST.dict()
            # cred = get_cred()
            # token_secret_key_1 = cred['token_secret_key_1']
            # token_secret_key_2 = cred['token_secret_key_2']
            # if input_json['token_secret_key_1'] == token_secret_key_1 and input_json['token_secret_key_2'] == token_secret_key_2:
            #     access_token = generate_access_token(input_json)
            #     refresh_token = generate_refresh_token(input_json)
            #     token_keys = dict(zip(['access_token', 'refresh_token'], [access_token, refresh_token]))
            #     output_json = dict(zip(["Status", "Message", "Payload"], [200, "User logged in successfully", token_keys]))

            #     return Response(output_json)
            pass
        except Exception as ex:
            pass
