import os
import yaml
import logging
from rest_framework.views import Response
from utilities.validator.views import schema_validation

logger = logging.getLogger(__name__)


def yaml_parser(yml):
    """Function for parsing Yaml File functionality."""
    data = {}  # assign
    with open(yml) as f:
        try:
            data = yaml.safe_load(f)
            logger.info(data)
        except yaml.YAMLError as exc:
            logger.info(exc)
    return data


def get_cred():
    """
        :param None:
        :return:
        """
    try:
        yml = yaml_parser(os.path.abspath('utilities/credmanager/credentials/credential.yaml'))
        p = os.path.abspath('utilities/credmanager/credentials/schema_credentials.json')
        schema_val = schema_validation(yml, p)
        if schema_val['Status'] == -1:
            return Response(schema_val)
        else:
            return yml

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure", f"Unable to fetch credentials: {ex}",
                                                                  None]))
        return output_json
