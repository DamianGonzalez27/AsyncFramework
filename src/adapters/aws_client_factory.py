"""Fábrica de clientes AWS para adaptadores."""

from hashlib import sha256
from threading import Lock

import boto3

from src.modules.clients.models.aws.aws_keys_model import AwsKeysModel


class AwsClientFactory:
    _sessions = {}
    _lock = Lock()

    @classmethod
    def get_client(
        cls,
        service_name: str,
        profile: str = "develop",
        region: str = "us-east-1",
    ):
        key = f"{profile}:{region}"
        with cls._lock:
            if key not in cls._sessions:
                cls._sessions[key] = boto3.Session(
                    profile_name=profile,
                    region_name=region,
                )
            session = cls._sessions[key]
            return session.client(service_name)

    @classmethod
    def get_client_v2(cls, aws_keys: AwsKeysModel):
        identity_seed = f"{aws_keys.access_key_id}:{aws_keys.region}"
        identity_hash = sha256(identity_seed.encode("utf-8")).hexdigest()

        with cls._lock:
            if identity_hash not in cls._sessions:
                cls._sessions[identity_hash] = boto3.Session(
                    aws_access_key_id=aws_keys.access_key_id,
                    aws_secret_access_key=aws_keys.secret_access_key,
                    region_name=aws_keys.region,
                )

            session = cls._sessions[identity_hash]
            return session.client(aws_keys.service_name)
