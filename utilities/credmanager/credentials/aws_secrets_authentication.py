from functools import wraps
import boto3
import base64
from botocore.exceptions import ClientError
import json

from utilities.credmanager.credentials.get_credentials import get_cred
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from django.utils.encoding import force_str
import logging
logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')
def aws_secrets_authentication(func):
    """Function to validate logout field."""
    @wraps(func)
    def aws_secrets_authentication_json(self, request):
        # AWS SECRETS MANAGER STARTS HERE
        logger_info.info("aws_secrets_authentication function called")
        secret_name = "dev/lpapp/seckey"
        region_name = "ap-south-1"
        cred = get_cred()
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=cred['aws_access_key_id'],
            aws_secret_access_key=cred['aws_secret_access_key']
        )

        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # We rethrow the exception by default.

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            output_json = dict(zip(["Status", "Message", "Payload"],
                                   ["452", f"Exception encountered while doing authentication: {e}", None]))
            
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                pass
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                pass
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                pass
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                pass
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                pass
            logger_error.error(str(e), exc_info=1)
            output_json['Response'] = str(e)
            return Response(output_json)
        else:
            # Decrypts secret using the associated KMS key.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = json.loads(get_secret_value_response['SecretString'])
                # if secret['SECRET_KEY'] == "$wy+dklnop1-mt$a2jtih&$ssh$k9lqy1_k+hiumc%rp$3s8)1":
                auth = get_authorization_header(request).split()

                if not (isinstance(auth, list)) or not auth:
                    output_json = dict(zip(["Status", "Message", "Payload"],
                                           ["452", "Invalid or Missing Authentication", None]))
                    return Response(output_json)

                # this is not for bearer token uncomment if you do not want beare token
                if secret['SECRET_KEY'] == force_str(auth[0]):
                    pass

                # this is  for bearer token uncomment if you want beare token
                # if secret['SECRET_KEY'] == force_str(auth[1]):
                #     pass
                else:
                    output_json = dict(zip(["Status", "Message", "Payload"],
                                           ["452", "Invalid Authentication", None]))
                    return Response(output_json)
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        return func(self, request)
    return aws_secrets_authentication_json

    # AWS SECRETS MANAGER ENDS HERE
