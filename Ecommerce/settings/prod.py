import os
from .common import *
load_dotenv()
# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')