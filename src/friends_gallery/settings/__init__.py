import os
from dotenv import load_dotenv
from .base import *

load_dotenv()

environment = os.getenv('ENVIRONMENT')

if environment == 'DEVELOPMENT':
    print(f"--- {environment} ENVIRONMENT ---")
    from .development import *
elif environment == 'PRODUCTION':
    print(f"--- {environment} ENVIRONMENT ---")
    from .production import *
else:
    print("--- UNKNOW ENVIRONMENT ---")
