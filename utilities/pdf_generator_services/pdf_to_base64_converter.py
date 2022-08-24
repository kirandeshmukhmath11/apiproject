import base64
import logging

logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')


def convert_pdf_to_base64(request, file):
    input_json = request
    service_name = input_json['service_name']
    service_request_id = input_json['service_request_id']
    logger_info.info(f"temporary pdf document generation from template initiated for {service_name} "
                     f"service with service request id = {service_request_id}")
    logger_info.info(f"base64 document generation from temporary pdf initiated for {service_name} service "
                     f"with service request id = {service_request_id}")
    try:
        file_path = file.replace('\\', '/')
        with open(file_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
            decoded = encoded_string.decode()
            base64_encoded_file_string = decoded

        logger_info.info(f"base64 document generation from temporary pdf completed for {service_name} service "
                         f"with service request id = {service_request_id}")
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [200, 'Base64 string from pdf file generated successfully',
                                base64_encoded_file_string]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [500, f"Exception Encountered {service_name} service call with "
                                     f"service_request_id as {service_request_id} while converting pdf to base64. "
                                     f"Exception is : {ex}", None]))
        return output_json
