from pydantic import BaseModel, Field

class AwsKeysModel(BaseModel):
    """
    Modelo de datos para representar las claves de acceso de AWS.

    Este modelo se utiliza para almacenar y validar las claves de acceso
    (Access Key ID y Secret Access Key) necesarias para autenticar
    operaciones contra los servicios de AWS. Es un modelo simple que
    encapsula la información esencial requerida para la autenticación.

    Importante:
        - Este modelo **NO** debe contener información sensible en texto
          plano en entornos de producción. Se recomienda utilizar mecanismos
          seguros para el almacenamiento y manejo de credenciales.
        - Su uso es exclusivamente interno, dentro de la capa de repositorios.
    """

    access_key_id: str = Field(
        ...,
        description="Clave de acceso (Access Key ID) de AWS.",
        examples=["AKIAIOSFODNN7EXAMPLE"]
    )

    secret_access_key: str = Field(
        ...,
        description="Clave secreta (Secret Access Key) de AWS.",
        examples=["wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"]
    )

    region: str = Field(
        ...,
        description="Región de AWS.",
        examples=["us-east-1"]
    )

    service_name: str = Field(
        ...,
        description="Nombre del servicio de AWS.",
        examples=["s3", "lambda", "ec2"]
    )
