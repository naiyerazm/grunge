import requests
from django.conf import settings
base_url = settings.HTTP_BASE_URL
def call_http(api_name=None,method_type="get",data={},headers={}):
    api_endpoint = base_url + api_name
    if method_type == 'get':
        r = requests.get(api_endpoint) 
    elif method_type == 'post':
        r = requests.post(api_endpoint,json=data)
    elif method_type == 'put':
        r = requests.put(api_endpoint,json=data)
    elif method_type == 'delete':
        r = requests.delete(api_endpoint)
    return r.json()