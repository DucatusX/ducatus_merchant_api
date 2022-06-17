import os
import yaml
from dataclasses import dataclass, field
from marshmallow_dataclass import class_schema
from typing import List, Dict


@dataclass
class Network:
    host: str
    port: int
    user: str
    password: str
    queue: str
    wallet_password: str
    polling_interval: int
    commitment_chain_length: int

@dataclass
class MailSettings:
    feedback_email: str
    default_from_email: str
    email_host: str
    email_host_user: str
    email_host_password: str
    email_port: int
    email_use_tls: bool

@dataclass
class Config:
    allowed_hosts: list
    secret_key: str
    debug: bool
    networks: Dict[str, Network]
    mail_settings: MailSettings
    rates_api_url: str

config_path = '/../config.yaml'

with open(os.path.dirname(__file__) + config_path) as f:
    config_data = yaml.safe_load(f)

config: Config = class_schema(Config)().load(config_data)