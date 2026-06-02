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
# expresa o implícita, incluyendo pero no limitado a garantías de
# comercialización, idoneidad para un propósito particular o ausencia
# de defectos.
# 
# El autor no será responsable por ningún daño directo o indirecto
# derivado del uso de este software.
# -------------------------

from botocore.client import BaseClient

from src.adapters.aws_client_factory import AwsClientFactory


# -------------------------
# Repositorio base para servicios AWS.
#
# Define una abstracción común para todos los repositorios que interactúan
# con servicios de AWS mediante boto3.
#
# Este repositorio:
# - No fija perfil ni región.
# - Permite trabajar de forma dinámica en múltiples cuentas y regiones.
# - Centraliza la obtención de clientes AWS.
#
# Los repositorios concretos deben enfocarse únicamente en la lógica
# del servicio (CloudFormation, ECS, S3, etc.).
# -------------------------
class BaseAwsRepository:

    # -------------------------
    # Inicializa el repositorio base de AWS.
    #
    # Args:
    #     service_name (str): Nombre del servicio AWS
    #         (por ejemplo: ``"cloudformation"``, ``"ecs"``, ``"s3"``).
    # -------------------------
    def __init__(self, service_name: str) -> None:
        self._service_name = service_name

    # -------------------------
    # Obtiene un cliente boto3 para el servicio configurado.
    #
    # El cliente se obtiene a través de la fábrica de clientes,
    # permitiendo reutilización de sesiones por perfil y región.
    #
    # Args:
    #     profile (str): Perfil de credenciales de AWS.
    #     region (str): Región de AWS.
    #
    # Returns:
    #     BaseClient: Cliente boto3 del servicio solicitado.
    # -------------------------
    def get_client(self, profile: str, region: str) -> BaseClient:
        return AwsClientFactory.get_client(
            service_name=self._service_name,
            profile=profile,
            region=region,
        )
