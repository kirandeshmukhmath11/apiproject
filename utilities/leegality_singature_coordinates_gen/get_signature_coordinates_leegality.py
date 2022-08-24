import copy
import json
# Loggers
import logging


logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')


def get_signature_coordinates_leegality(request):
    input_json = request
    service_name = input_json['service_name']
    service_request_id = input_json['service_request_id']
    try:
        logger_info.info(f"{service_name} service signature coordinates calculation initiated. "
                         f"service request id = {service_request_id}")

        coordinates_var_list = None
        if 'coordinates' in input_json['placement_var'].keys():
            coordinates_var_list = []
            if input_json['placement_var']['coordinates']['type'].lower() in ["static", "fixed"]:
                for item in input_json['placement_var']['coordinates']['invitees']:
                    coordinates_var = item
                    if item['party_in_doc_params'] == "Yes":
                        coordinates_var['name'] = eval(f"input_json['input_vars']{item['name']}")
                        coordinates_var['email'] = eval(f"input_json['input_vars']{item['email']}")
                        coordinates_var['phone'] = eval(f"input_json['input_vars']{item['phone']}")
                    coordinates_var_list.append(coordinates_var)
            elif input_json['placement_var']['coordinates']['type'].lower() in ["dynamic", "variable"]:
                dynamic_coordinates_var = get_dynamic_signature_coordinates_leegality(input_json)
                if dynamic_coordinates_var['Status'] != 200:
                    return dynamic_coordinates_var
                coordinates_var_list = dynamic_coordinates_var['Payload']
            else:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       [452, f"invalid coordinates configured in for given doctype for "
                                             f" {service_name} service call with "
                                             f"service_request_id as {service_request_id}. Value of coordinate type "
                                             f"must be either 'static' or 'fixed' or 'dynamic' or 'variable'",
                                        coordinates_var_list]))
                return output_json

        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [200, f"Signature coordinates generated successfully for "
                                     f" {service_name} service call with "
                                     f"service_request_id as {service_request_id} ",
                                coordinates_var_list]))
        return output_json

    except Exception as ex:
        logger_error.error(f"Exception Encountered  while generating signature coordinates in {service_name} "
                           f"service call with service_request_id as {service_request_id}. "
                           f"Exception is : {ex}", exc_info=1)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [500, f"Exception Encountered  while generating signature coordinates in {service_name} "
                                     f"service call with service_request_id as {service_request_id}. "
                                     f"Exception is : {ex}", None]))
        return output_json


def get_dynamic_signature_coordinates_leegality(request):
    input_json = request
    service_name = input_json['service_name']
    service_request_id = input_json['service_request_id']
    try:
        pointer_page, pointer_y_coordinate, coordinates_var_list, line_height = 1, {"page": 0, "y_c": 780}, [], 10
        for item in input_json['placement_var']['coordinates']['sections']:
            if item['section_type'].lower() == "static":
                pointer_page += int(item['section_length_pages'])
                pointer_y_coordinate['page'] += int(pointer_page)

                if pointer_y_coordinate['y_c'] - int(item['section_length_lines'])*line_height <= 0:
                    pointer_y_coordinate['page'] += (int(pointer_y_coordinate['y_c'])
                                                     - int(pointer_y_coordinate['y_c']) % 780) / 780
                    pointer_y_coordinate['y_c'] = 780 - (pointer_y_coordinate['y_c']
                                                         - int(item['section_length_lines'])*line_height)
                else:
                    pointer_y_coordinate['y_c'] -= int(item['section_length_lines']) * line_height
            elif item['section_type'].lower() == "dynamic":
                for jitem in item['invitees']:
                    coordinates_var = jitem
                    if pointer_y_coordinate['y_c'] - float(jitem['lines_from_last_content']) * line_height <= 0:
                        pointer_y_coordinate['page'] += 1
                        pointer_y_coordinate['y_c'] = 780 - (float(jitem['lines_from_last_content']) * line_height
                                                             - pointer_y_coordinate['y_c'])

                    # pointer_y_coordinate += float(jitem['lines_from_last_content']*line_height)

                    if jitem['party_in_doc_params'] == "Yes":

                        if jitem['party_in_doc_params_type'] != "list":
                            party_list = [eval(f"input_json['input_vars']{jitem['item_to_pick']}")]
                        else:
                            party_list = eval(f"input_json['input_vars']{jitem['item_to_pick']}")
                        counter = 0
                        for kitem in party_list:
                            lines_from_last_content = jitem['section_height_in_lines']
                            if counter == 0:
                                lines_from_last_content = jitem['lines_from_last_content']
                                counter += 1
                            pointer_y_coordinate['y_c'] -= float(lines_from_last_content)*line_height
                            print(kitem)
                            coordinates_var['name'] = kitem['name']
                            coordinates_var['email'] = kitem['email']
                            coordinates_var['phone'] = kitem['phone']
                            var_y1 = pointer_y_coordinate['y_c']

                            if pointer_y_coordinate['y_c'] - float(lines_from_last_content) * line_height <= 0:
                                pointer_y_coordinate['page'] += 1
                                print(f"Val 103 = {pointer_y_coordinate['y_c']}")
                                pointer_y_coordinate['y_c'] = 780 \
                                                              - (float(lines_from_last_content) * line_height
                                                                 - pointer_y_coordinate['y_c'])
                                print(f"Val 106 = {float(lines_from_last_content)}")
                                print(f"Val 107 = {float(lines_from_last_content) * line_height}")
                                print(f"Val 108 = {pointer_y_coordinate['y_c']}")
                            else:
                                pointer_y_coordinate['y_c'] -= float(lines_from_last_content) * line_height
                            y1_var = 0
                            if pointer_y_coordinate['y_c'] >= 50:
                                y1_var = pointer_y_coordinate['y_c']-50

                            coordinates_var['appearances'] = [
                                {
                                    "x1": jitem['x1'],
                                    "x2": jitem['x2'],
                                    "y1": y1_var,
                                    "y2": pointer_y_coordinate['y_c'],
                                    "page": pointer_y_coordinate['page']
                                }
                            ]
                            coordinates_var_deep_copy = copy.deepcopy(coordinates_var)
                            coordinates_var_deep_copy.pop('party_in_doc_params')
                            # coordinates_var_deep_copy.pop('party_in_doc_params_type')
                            coordinates_var_deep_copy.pop('item_to_pick')
                            coordinates_var_deep_copy.pop('lines_from_last_content')
                            coordinates_var_deep_copy.pop('x1')
                            coordinates_var_deep_copy.pop('x2')
                            coordinates_var_deep_copy.pop('party_in_doc_params_type')

                            coordinates_var_list.append(coordinates_var_deep_copy)
            else:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       [452, f"invalid dynamic coordinates configured in for given doctype for "
                                             f" {service_name} service call with "
                                             f"service_request_id as {service_request_id}. Value of coordinate type "
                                             f"must be either 'static' or 'fixed' or 'dynamic' or 'variable'",
                                        coordinates_var_list]))
                return output_json

        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [200, f"Dynamic Signature coordinates generated successfully for "
                                     f" {service_name} service call with "
                                     f"service_request_id as {service_request_id} ",
                                coordinates_var_list]))
        return output_json
    except Exception as ex:
        logger_error.error(f"Exception Encountered  while generating dynamic signature coordinates in {service_name} "
                           f"service call with service_request_id as {service_request_id}. "
                           f"Exception is : {ex}", exc_info=1)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [500, f"Exception Encountered  while generating dynamic signature coordinates in "
                                     f"{service_name} service call with service_request_id as {service_request_id}. "
                                     f"Exception is : {ex}", None]))
        return output_json
