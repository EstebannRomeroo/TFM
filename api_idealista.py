import requests
import os
from dotenv import load_dotenv

load_dotenv()

# for key, value in os.environ.items():
#     print(key, value)

client_id = os.getenv("CLIENT_ID")
print(f'CLIENT_ID = {client_id}')


