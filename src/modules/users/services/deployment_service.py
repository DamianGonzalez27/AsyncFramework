import os
from botocore.exceptions import ClientError
from logger_tracker import logg_debug, logg_info
from src.modules.clients.models.http.service_response import ServiceResponse
from src.modules.clients.models.http.deploy_stack_request import DeployRequest

class DeploymentService:
    def __init__(self, aws_repository):
        self.aws_repository = aws_repository

    def deploy_local_stack(self, deployment_request: DeployRequest):
        template_file_path = os.path.join("templates",deployment_request.environment, deployment_request.base_path, deployment_request.template_file)
        stack_name = deployment_request.stack_name
        self.aws_repository.use_profile('cloudformation', deployment_request.environment, deployment_request.region)
        parameters = {
            "DeployVersion": deployment_request.deploy_version
        }
        logg_info("🚀 deploy_local_stack")
        logg_info(f"Template File Path: {template_file_path}")
        logg_info(f"Stack Name: {stack_name}")
        stack_exists = False
        try:
            with open(template_file_path, "r") as template_file:
                template_body = template_file.read()
                logg_debug(f"Template Body: {template_body[:100]}...")
        except FileNotFoundError:
            logg_info(f"❌ Error: El archivo de plantilla {template_file_path} no fue encontrado.")
            return ServiceResponse(False, f"Archivo de plantilla {template_file_path} no encontrado.", 400)
        try:
            self.aws_repository.describe_stacks(stack_name)
            stack_exists = True
        except ClientError as e:
            if "does not exist" in str(e):
                logg_info(f"Stack {stack_name} no existe. Procediendo a crear uno nuevo.")
                stack_exists = False
        if stack_exists:
            logg_info(f"🔄 Intentando actualizar stack existente: {stack_name}...")
            try:
                self.aws_repository.update_stack(stack_name, template_body, parameters)
                # waiter = self.aws_repository.get_waiter('stack_update_complete')
            except ClientError as e:
                logg_info(f"ClientError: {e}")
                if "No updates are to be performed" in str(e):
                    logg_info(f"✅ Stack {stack_name} ya está actualizado. No se requiere acción.")
                    return ServiceResponse(True, f"Stack {stack_name} ya está actualizado. No se requiere acción.", 202)
                else:
                    return ServiceResponse(False, f"Error al actualizar stack {stack_name}", 400)
        else:
            try:
                logg_info(f"✨ Creando nuevo stack: {stack_name}...")
                self.aws_repository.create_stack(stack_name, template_body, parameters)
                # waiter = self.aws_repository.get_waiter('stack_create_complete')
            except ClientError as e:
                logg_info(f"ClientError: {e}")
                return ServiceResponse(False, f"Error al desplegar {stack_name}: {e}", 400)
            
        logg_info("⏳ Esperando a que el despliegue finalice...")
        # waiter.wait(StackName=stack_name)
        logg_info(f"✅ {stack_name} desplegado con éxito.")
        return ServiceResponse(True, f"Stack {stack_name} desplegado con éxito.", 200)
