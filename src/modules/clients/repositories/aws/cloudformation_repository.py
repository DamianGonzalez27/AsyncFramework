
# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
#
# Este software y su código fuente han sido desarrollados por Erick Damian Gonzalez Aranda, mediante 
# NeuronexoTec Organizacion de desarrollo de Software.
# Todos los derechos están reservados.
#
# Se permite el uso, copia y modificación del código únicamente para fines
# personales, educativos o internos, siempre que se conserve este aviso
# de copyright y no se redistribuya el software, total o parcialmente,
# sin autorización expresa del autor.
#
# Queda estrictamente prohibida la venta, sublicencia, redistribución,
# exposición como servicio (SaaS), o incorporación en productos comerciales
# sin consentimiento previo y por escrito del autor.
#
# Este software se proporciona "tal cual", sin garantía de ningún tipo,
# expresa o implícita.
# -------------------------
from typing import Dict, Optional, Any, List

from botocore.exceptions import ClientError

from src.modules.clients.repositories.aws.aws_base_repository import BaseAwsRepository
from src.modules.clients.models.aws.cloudformation.create_stack_cloudformation import CreateStackModel
from src.modules.clients.models.aws.cloudformation.create_stack_cloudformation import UpdateStackRequest
from logger_tracker import logg_info, logg_error, logg_debug

from src.config import CAPABILITIES

# -------------------------
# Repositorio para la gestión de stacks de AWS CloudFormation.
#
# Proporciona una abstracción para crear, actualizar y eliminar
# stacks de CloudFormation utilizando boto3, encapsulando
# la interacción directa con el cliente AWS.
# -------------------------
class CloudFormationRepository(BaseAwsRepository):

    # -------------------------
    # Inicializa el repositorio de CloudFormation.
    #
    #     Args:
    #         profile (str, optional): Perfil de credenciales de AWS.
    #             Defaults to ``"develop"``.
    #         region (str, optional): Región de AWS.
    #             Defaults to ``"us-east-1"``.
    # -------------------------
    def __init__(self) -> None:
        super().__init__(service_name="cloudformation")

    # -------------------------
    # Obtiene un cliente de CloudFormation para el perfil y región indicados.
    #
    #     Args:
    #         profile (str): Perfil de credenciales de AWS.
    #         region (str): Región de AWS.
    #
    #     Returns:
    #         boto3.client: Cliente de CloudFormation.
    # -------------------------
    def _get_client(self, profile: str, region: str):
        return self.get_client(profile=profile, region=region)

    def create_stack(
        self,
        create_stack: CreateStackModel
    ) -> Dict[str, Any]:
        logg_info("start: create_stack AwsRepository")
        client = self._get_client(
            create_stack.profile,
            create_stack.region,
        )
        if create_stack.template_body and create_stack.template_url:
            raise ValueError(
                "Solo se puede usar uno: template_body o template_url."
            )
        
        args = {
            "StackName": create_stack.stack_name,
            "Capabilities": create_stack.capabilities or CAPABILITIES,
            "Tags": [
                {"Key": k, "Value": v}
                for k, v in (create_stack.tags or {}).items()
            ],
        }

        if create_stack.template_body:
            args["TemplateBody"] = create_stack.template_body
        elif create_stack.template_url:
            args["TemplateURL"] = create_stack.template_url
        else:
            raise ValueError(
                "Debes proporcionar template_body o template_url."
            )

        if create_stack.parameters:
            args["Parameters"] = [
                {
                    "ParameterKey": p["ParameterKey"],
                    "ParameterValue": p["ParameterValue"],
                }
                for p in create_stack.parameters
            ]

        try:
            response = client.create_stack(**args)
            logg_info("success: create_stack AwsRepository")
            return response

        except ClientError as exc:
            logg_error("error: create_stack AwsRepository")
            raise
    
    def update_stack(
        self,
        request: UpdateStackRequest,
    ) -> Dict[str, Any]:
        logg_info("start: update_stack AwsRepository")

        client = self._get_client(request.profile, request.region)

        if request.template_body and request.template_url:
            raise ValueError(
                "Solo se puede usar uno: template_body o template_url."
            )

        payload: Dict[str, Any] = {
            "StackName": request.stack_name,
            "Capabilities": request.capabilities or CAPABILITIES,
            "Tags": [
                {"Key": k, "Value": v}
                for k, v in request.tags.items()
            ],
        }

        if request.template_body:
            payload["TemplateBody"] = request.template_body
        elif request.template_url:
            payload["TemplateURL"] = request.template_url
        else:
            payload["UsePreviousTemplate"] = True
        
        boto_parameters = []

        for param in request.parameters:
            boto_parameters.append({
                "ParameterKey": param["ParameterKey"],
                "ParameterValue": param["ParameterValue"],
            })

        if boto_parameters:
            payload["Parameters"] = boto_parameters

        try:
            response = client.update_stack(**payload)
            logg_info("success: update_stack AwsRepository")
            return response

        except ClientError as exc:
            if "No updates are to be performed" in str(exc):
                logg_info("no changes detected for stack update")
                return {
                    "status": "NO_CHANGES",
                    "stack_name": request.stack_name,
                }
            raise

    def delete_stack(
        self,
        profile: str,
        region: str,
        stack_name: str,
    ) -> None:
        client = self._get_client(profile, region)

        try:
            client.delete_stack(StackName=stack_name)
        except ClientError as exc:
            raise exc
        
    # ------------------------------------------------------------------
    # Consultas y estado
    # ------------------------------------------------------------------

    def describe_stacks(
        self,
        profile: str,
        region: str,
        stack_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Obtiene información de uno o varios stacks.
        """
        client = self._get_client(profile, region)

        try:
            if stack_name:
                return client.describe_stacks(StackName=stack_name)
            return client.describe_stacks()
        except ClientError as exc:
            raise exc

    def describe_stack_events(
        self,
        profile: str,
        region: str,
        stack_name: str,
    ) -> Dict[str, Any]:
        """
        Obtiene los eventos de un stack.
        """
        client = self._get_client(profile, region)

        try:
            return client.describe_stack_events(StackName=stack_name)
        except ClientError as exc:
            raise exc

    def describe_stack_resources(
        self,
        profile: str,
        region: str,
        stack_name: str,
    ) -> Dict[str, Any]:
        """
        Obtiene los recursos asociados a un stack.
        """
        client = self._get_client(profile, region)

        try:
            return client.describe_stack_resources(StackName=stack_name)
        except ClientError as exc:
            raise exc

    def get_template(
        self,
        profile: str,
        region: str,
        stack_name: str,
    ) -> Dict[str, Any]:
        """
        Obtiene el template asociado a un stack.
        """
        client = self._get_client(profile, region)

        try:
            return client.get_template(StackName=stack_name)
        except ClientError as exc:
            raise exc

    def get_template_summary(
        self,
        profile: str,
        region: str,
        template_body: str,
    ) -> Dict[str, Any]:
        """
        Obtiene un resumen del template de CloudFormation.
        """
        client = self._get_client(profile, region)

        try:
            return client.get_template_summary(TemplateBody=template_body)
        except ClientError as exc:
            raise exc

    # ------------------------------------------------------------------
    # Validación
    # ------------------------------------------------------------------

    def validate_template(
        self,
        profile: str,
        region: str,
        template_body: str,
    ) -> Dict[str, Any]:
        """
        Valida un template de CloudFormation sin desplegarlo.
        """
        client = self._get_client(profile, region)

        try:
            return client.validate_template(TemplateBody=template_body)
        except ClientError as exc:
            raise exc

    # ------------------------------------------------------------------
    # Change Sets
    # ------------------------------------------------------------------

    def create_change_set(
        self,
        profile: str,
        region: str,
        stack_name: str,
        change_set_name: str,
        template_body: str,
        parameters: Optional[List[Dict[str, Any]]] = None,
        capabilities: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Crea un Change Set para un stack.
        """
        client = self._get_client(profile, region)

        try:
            return client.create_change_set(
                StackName=stack_name,
                ChangeSetName=change_set_name,
                TemplateBody=template_body,
                Parameters=parameters or [],
                Capabilities=capabilities or [],
            )
        except ClientError as exc:
            raise exc

    def describe_change_set(
        self,
        profile: str,
        region: str,
        change_set_name: str,
        stack_name: str,
    ) -> Dict[str, Any]:
        """
        Obtiene el detalle de un Change Set.
        """
        client = self._get_client(profile, region)

        try:
            return client.describe_change_set(
                ChangeSetName=change_set_name,
                StackName=stack_name,
            )
        except ClientError as exc:
            raise exc

    def execute_change_set(
        self,
        profile: str,
        region: str,
        change_set_name: str,
        stack_name: str,
    ) -> None:
        """
        Ejecuta un Change Set.
        """
        client = self._get_client(profile, region)

        try:
            client.execute_change_set(
                ChangeSetName=change_set_name,
                StackName=stack_name,
            )
        except ClientError as exc:
            raise exc

    def delete_change_set(
        self,
        profile: str,
        region: str,
        change_set_name: str,
        stack_name: str,
    ) -> None:
        """
        Elimina un Change Set.
        """
        client = self._get_client(profile, region)

        try:
            client.delete_change_set(
                ChangeSetName=change_set_name,
                StackName=stack_name,
            )
        except ClientError as exc:
            raise exc

    # ------------------------------------------------------------------
    # Drift
    # ------------------------------------------------------------------

    def detect_stack_drift(
        self,
        profile: str,
        region: str,
        stack_name: str,
    ) -> Dict[str, Any]:
        """
        Inicia la detección de drift de un stack.
        """
        client = self._get_client(profile, region)

        try:
            return client.detect_stack_drift(StackName=stack_name)
        except ClientError as exc:
            raise exc

    def describe_stack_drift_detection_status(
        self,
        profile: str,
        region: str,
        stack_drift_detection_id: str,
    ) -> Dict[str, Any]:
        """
        Consulta el estado de una detección de drift.
        """
        client = self._get_client(profile, region)

        try:
            return client.describe_stack_drift_detection_status(
                StackDriftDetectionId=stack_drift_detection_id
            )
        except ClientError as exc:
            raise exc

    def describe_stack_resource_drifts(
        self,
        profile: str,
        region: str,
        stack_name: str,
    ) -> Dict[str, Any]:
        """
        Obtiene los drifts de recursos de un stack.
        """
        client = self._get_client(profile, region)

        try:
            return client.describe_stack_resource_drifts(
                StackName=stack_name
            )
        except ClientError as exc:
            raise exc
