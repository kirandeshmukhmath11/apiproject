import logging
logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')


def validate_docparams_with_schema(request):
    input_json = request
    service_name = input_json['service_name']
    service_request_id = input_json['service_request_id']
    try:
        logger_info.info(f"Validation initiated for {service_name} service call with "
                         f"service_request_id as {service_request_id} ", exc_info=1)
        for item in input_json['schema_params'].keys():
            if item == 'required_list':
                list_validations_params = dict(
                    zip(['service_name', 'service_request_id', 'schema_params', 'input_params', 'level'],
                        [service_name, service_request_id, input_json['schema_params'][item],
                         input_json['input_params'],
                         f"{input_json['level']}.{item}"]))
                list_validation_output = validate_list_schema(list_validations_params)
                if list_validation_output['Status'] in [452, 500]:
                    output_json = list_validation_output
                    return output_json
            if isinstance(input_json['schema_params'][item], list):
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       [452, f"lists are not allowed in {service_name} service call with "
                                             f"service_request_id as {service_request_id} unless the key is named - required_lists",
                                        f"{input_json['level']}.{item}"]))
                return output_json
            if item != 'required_list' and isinstance(input_json['schema_params'][item], dict):
                if item not in input_json['input_params'].keys():
                    output_json = dict(zip(['Status', 'Message', 'Payload'],
                                           [452, f"missing dictionary in {service_name} service call with "
                                                 f"service_request_id as {service_request_id} ",
                                            f"{input_json['level']}.{item}"]))
                    return output_json
                validations_params = dict(
                    zip(['service_name', 'service_request_id', 'schema_params', 'input_params', 'level'],
                        [service_name, service_request_id, input_json['schema_params'][item], input_json['input_params'][item],
                         f"{input_json['level']}.{item}"]))
                validation_output = validate_docparams_with_schema(validations_params)
                if validation_output['Status'] in [452, 500]:
                    return validation_output
            else:
                if input_json['schema_params'][item] == "required":
                    if item not in input_json['input_params'].keys():
                        output_json = dict(zip(['Status', 'Message', 'Payload'],
                                               [452, f"missing mandatory item {service_name} service call with "
                                                     f"service_request_id as {service_request_id} ", f"{input_json['level']}.{item}"]))
                        return output_json
                    if input_json['input_params'][item] in [None, ""]:
                        output_json = dict(zip(['Status', 'Message', 'Payload'],
                                               [452, f"missing value of mandatory item {service_name} service call with "
                                                     f"service_request_id as {service_request_id} ", f"{input_json['level']}.{item}"]))
                        return output_json
        logger_info.info(f"Validation successful for {service_name} service call with "
                           f"service_request_id as {service_request_id} at {input_json['level']}",
                           exc_info=1)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [200, f"Validation successful for {service_name} service call with "
                                     f"service_request_id as {service_request_id} ", None]))
        return output_json
    except Exception as ex:
        logger_error.error(f"Exception Encountered {service_name} service call with "
                           f"service_request_id as {service_request_id} while validating input. Exception is : {ex}", exc_info=1)
        output_json = dict(zip(['Status', 'Message',  'Payload'],
                               [500, f"Exception Encountered {service_name} service call with "
                                     f"service_request_id as {service_request_id}. Exception is : {ex}. "
                                     f"service input at breakpoint: {input_json['schema_params'][item]}"
                                     f"INPUT_PARAMS = {input_json['input_params']}", None]))
        return output_json


def validate_list_schema(request):
    input_json = request
    service_name = input_json['service_name']
    service_request_id = input_json['service_request_id']
    try:
        logger_info.info(f"Required list validation initiated for {service_name} service call with "
                         f"service_request_id as {service_request_id} ", exc_info=1)

        # checking if keys of the given list of dictionary matches with that in the schema
        required_list_required_keys_set = set([x for x in input_json['schema_params'].keys() if input_json['schema_params'][x] == "required"])
        if not isinstance(input_json['input_params'], list):
            logger_error.error(f"dictionary passed in input instead of a list of dictionary for {service_name} "
                               f"service call with service_request_id as {service_request_id}: {input_json['level']}",
                               exc_info=1)
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   [452, f"dictionary passed in input instead of a list of dictionary for {service_name} "
                                         f"service call with service_request_id as {service_request_id}: {input_json['level']}", None]))
            return output_json
        for item in input_json['input_params']:
            item_keys_set = set(item.keys())
            if not required_list_required_keys_set.issubset(item_keys_set):
                logger_error.error(f"Required list of dictionary not matching with schema for {service_name} "
                                   f"service call with service_request_id as {service_request_id}: {input_json['level']}"
                                   f"item in consideration is : {item} for list: {input_json['input_params']}",
                                   exc_info=1)
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       [452, f"Required list of dictionary not matching with schema for {service_name} "
                                             f"service call with service_request_id as "
                                             f"{service_request_id}: {input_json['level']}. "
                                             f"item in consideration is : {item} for list: {input_json['input_params']} "
                                             f"required dictionary within list must be following the schema: "
                                             f"{input_json['schema_params']}",
                                        None]))
                return output_json
        logger_info.info(f"Required list of dictionary validated with schema for {service_name} "
                           f"service call with service_request_id as {service_request_id}: {input_json['level']}",
                           exc_info=1)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               [200, f"Required list of dictionary validated  with schema for {service_name} "
                                     f"service call with service_request_id as "
                                     f"{service_request_id}: {input_json['level']}"
                                     f"required dictionary within list must be following the schema: "
                                     f"{input_json['schema_params']}", None]))
        return output_json

    except Exception as ex:
        logger_error.error(f"Exception Encountered while validating required list {service_name} service call with "
                           f"service_request_id as {service_request_id} while validating input. "
                           f"Exception is : {ex}", exc_info=1)
        output_json = dict(zip(['Status', 'Message',  'Payload'],
                               [500, f"Exception Encountered  while validating required list {service_name} "
                                     f"service call with service_request_id as {service_request_id}. "
                                     f"Exception is : {ex}", None]))
        return output_json


