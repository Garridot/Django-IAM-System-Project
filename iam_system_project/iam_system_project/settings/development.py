# iam_system_project/settings/development.py
from .base import *

DEBUG = env('DEBUG_DEVELOPMENT', default=True)
ALLOWED_HOSTS = [env('ALLOWED_HOSTS_DEVELOPMENT', default='localhost')]
