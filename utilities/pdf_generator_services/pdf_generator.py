import os
import logging
from io import BytesIO
from xhtml2pdf import pisa
# import datetime
from datetime import datetime
from utilities.pdf_generator_services.pdf_to_base64_converter import convert_pdf_to_base64

logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')


def render_to_pdf(request, template_src, context_dict={}):
    input_json = request
    service_name = input_json['service_name']
    service_request_id = input_json['service_request_id']
    logger_info.info(f"temporary pdf document generation from template initiated for {service_name} "
                     f"service with service request id = {service_request_id}")
    try:
        template = template_src
        html = template.render(context_dict)

        # Storing file in local storage
        settings_dir = os.path.dirname(__file__)
        PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
        DOWNLOAD_APPLICATION_FOLDER = os.path.join(PROJECT_ROOT, 'tempfilefolder')
        now = datetime.now()
        today_time = str(now)[0:19]
        today_time = today_time.replace(' ', '-')
        today_time = today_time.replace(':', '-')
        file_name = f"mypdf{today_time}.pdf"
        file_full_path = f"{DOWNLOAD_APPLICATION_FOLDER}/{file_name}"
        logger_info.info(f"temporary pdf document generation from template generated for {service_name} service "
                         f"with service request id = {service_request_id}")

        with open(file_full_path, 'wb+') as result:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

            # Closing the file connection
            result.close()
            # Function call to convert file type to base64 encoded file string
            base64_output = convert_pdf_to_base64(input_json, file_full_path)
            if base64_output['Status'] != 200:
                return base64_output
            base64_encoded_file_string = base64_output['Payload']

            # Deleting file from local storage
            os.remove(file_full_path)
            logger_info.info(f"temporary pdf document deleted from storage for {service_name} service "
                             f"with service request id = {service_request_id}")
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   [200, 'PDF file generated successfully',
                                    base64_encoded_file_string]))
        return output_json

    except Exception as ex:
        logger_error.error(f"Exception Encountered {service_name} service call with "
                           f"service_request_id as {service_request_id} while generating pdf file "
                           f"or while converting it to base64. Exception is : {ex}",
                           exc_info=1)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [500, f"Exception Encountered {service_name} service call with "
                                     f"service_request_id as {service_request_id} while generating pdf file "
                                     f"or while converting it to base64.  Exception is : {ex}", None]))
        return output_json
