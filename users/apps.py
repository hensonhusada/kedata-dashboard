from django.apps import AppConfig
from users.rpc_client import RpcClient

class UsersConfig(AppConfig):
    name = 'users'