from logger_tracker import logg_info
from src.config import CAPABILITIES
from src.adapters.aws_client_factory import AwsClientFactory

class AwsRepository:
    def __init__(self, client_factory=None):
        self.client_factory = client_factory or AwsClientFactory.get_client
        self.aws_client = None

    def use_profile(self, service_name, profile, region="us-east-1"):
        self.aws_client = self.client_factory(service_name, profile, region)
        return self.aws_client

    def create_stack(self, stack_name, template_file_path, parameters=None):
        logg_info("start: create_stack AwsRepository")
        boto3_parameters = []
        if parameters:
            for key, value in parameters.items():
                boto3_parameters.append({
                    'ParameterKey': key,
                    'ParameterValue': value
                })
        args = {
            'StackName': stack_name,
            'TemplateBody': template_file_path,
            'Capabilities': CAPABILITIES
        }
        if boto3_parameters:
            args['Parameters'] = boto3_parameters
        self.aws_client.create_stack(**args)
        logg_info("success: create_stack AwsRepository")
        return True

    def update_stack(self, stack_name, template_file_path, parameters=None):
        logg_info("start: update_stack AwsRepository")
        boto3_parameters = []
        if parameters:
            for key, value in parameters.items():
                boto3_parameters.append({
                    'ParameterKey': key,
                    'ParameterValue': value
                })
        args = {
            'StackName': stack_name,
            'TemplateBody': template_file_path,
            'Capabilities': CAPABILITIES
        }
        if boto3_parameters:
            args['Parameters'] = boto3_parameters
        self.aws_client.update_stack(**args)
        logg_info("success: update_stack AwsRepository")
        return True

    def describe_stacks(self, stack_name):
        logg_info("start: describe_stacks AwsRepository")
        return self.aws_client.describe_stacks(StackName=stack_name)

    def get_waiter(self, waiter_name):
        logg_info("start: get_waiter AwsRepository")
        return self.aws_client.get_waiter(waiter_name)
