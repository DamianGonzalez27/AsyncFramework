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

from typing import Dict, List, Optional
from pydantic import Field

from src.modules.clients.models.aws.aws_base_model import AwsBaseModel


class CreateStackModel(AwsBaseModel):

    # -------------------------
    # Datos del stack
    # -------------------------
    stack_name: str = Field(
        ...,
        description="Nombre único del stack de CloudFormation.",
    )

    template_body: Optional[str] = Field(
        None,
        description="Plantilla CloudFormation en formato JSON o YAML como string.",
    )

    template_url: Optional[str] = Field(
        None,
        description="URL de la plantilla CloudFormation almacenada en S3.",
    )

    parameters: List[Dict[str, str]] = Field(
        default_factory=list,
        description=(
            "Lista de parámetros que se pasarán a la plantilla de CloudFormation. "
            "Cada parámetro debe contener ParameterKey y ParameterValue."
        ),
    )

    capabilities: List[str] = Field(
        default_factory=list,
        description=(
            "Lista de capacidades requeridas por el stack "
            "(por ejemplo: CAPABILITY_NAMED_IAM)."
        ),
    )

    tags: Dict[str, str] = Field(
        default_factory=dict,
        description="Etiquetas que se asignarán al stack.",
    )

    on_failure: str = Field(
        default="ROLLBACK",
        description=(
            "Acción a ejecutar si falla la creación del stack "
            "(DO_NOTHING | ROLLBACK | DELETE)."
        ),
    )

    class Config:
        """
        Configuración del modelo.
        """
        frozen = True
