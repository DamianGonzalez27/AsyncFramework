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


class UpdateStackRequest(AwsBaseModel):

    stack_name: str

    template_body: Optional[str] = None
    template_url: Optional[str] = None

    parameters: List[Dict[str, str]] = Field(
        default_factory=list,
        description=(
            "Parámetros nuevos o existentes. "
            "Si un parámetro no viene, se mantiene con UsePreviousValue."
        ),
    )

    capabilities: List[str] = Field(default_factory=list)

    tags: Dict[str, str] = Field(default_factory=dict)

    class Config:
        frozen = True
