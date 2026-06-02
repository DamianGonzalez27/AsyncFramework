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

from pydantic import BaseModel, Field


class AwsBaseModel(BaseModel):
    """
    Modelo base que representa el contexto de ejecución para cualquier
    operación contra servicios de AWS.

    Este modelo define los parámetros mínimos y obligatorios necesarios
    para interactuar con AWS mediante boto3, y está diseñado para ser
    reutilizado por todos los repositorios de servicios AWS
    (CloudFormation, ECS, S3, IAM, etc.).

    Importante:
        - Este modelo **NO** está ligado a HTTP, controladores o APIs.
        - Su uso es exclusivamente interno, dentro de la capa de repositorios.
    """

    profile: str = Field(
        ...,
        description=(
            "Nombre del perfil de credenciales de AWS que se utilizará "
            "para ejecutar la operación."
        ),
        examples=["develop", "staging", "production"],
    )

    region: str = Field(
        ...,
        description=(
            "Región de AWS donde se ejecutará la operación "
            "(por ejemplo: us-east-1, eu-west-1)."
        ),
        examples=["us-east-1", "us-west-2"],
    )

    class Config:
        """
        Configuración base del modelo Pydantic.
        """
        frozen = True
