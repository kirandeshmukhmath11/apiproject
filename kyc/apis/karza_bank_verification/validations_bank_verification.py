import os
import logging
import uuid
from functools import wraps
from rest_framework.views import Response
from utilities.validator.views import schema_validation
logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')


def validations_bank_verification_schema(func):
    """Function to validate logout field."""
    @wraps(func)
    def validations_bank_verification_json(self, request):
        """
            :param None:
            :return:
            """
        validation_service_request_id = uuid.uuid1()
        # ######################################################
        # Configure the below piece for validations
        # ######################################################
        validation_service_name = "Bank Verification"
        p = os.path.abspath('kyc/apis/karza_bank_verification/schema_bank_verification.json')
        # ######################################################################################
        # Configure the above piece for validations. No need to change anything below this line
        # ######################################################################################

        try:
            logger_info.info(f"{validation_service_name} validation function initiated with "
                             f"validation_service_request_id as {validation_service_request_id}")
            data = request.data
            schema_val = schema_validation(data, p)
            if schema_val['Status'] == 452:
                logger_info.info(f"{validation_service_name} validation failed with "
                                 f"validation_service_request_id as {validation_service_request_id}")
                return Response(schema_val)
            else:
                pass

        except Exception as ex:
            logger_error.error(f"Exception Encountered {validation_service_name} service call with "
                               f"service_request_id as {validation_service_request_id}. Exception is : {ex}", exc_info=1)
            output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure", f"Unable to fetch data: {ex}",
                                                                      None]))
            return Response(output_json)
        logger_info.info(f"{validation_service_name} validation function successfully passed with "
                         f"validation_service_request_id as {validation_service_request_id}")
        return func(self, request)

    return validations_bank_verification_json
