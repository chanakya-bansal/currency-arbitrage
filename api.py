from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

  
base_url="https://api.exchangerate.host/"  
api_key = os.getenv("API_KEY")

request=base_url+"live"+"?access_key="+api_key
#data = requests.get(request).json()

print(f"request: {request}")


with open("live.json", "w") as f:
    json.dump(data,f,indent=4)

print("successfully executed");