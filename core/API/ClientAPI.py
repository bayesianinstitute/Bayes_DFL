import requests

class ApiClient:
    def __init__(self, ip='http://127.0.0.1',port=8000):
        self.base_url = f'{ip}:{port}/api/v1'

    def get_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        return response

    def post_request(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }
        print(data)
        response = requests.post(url, json=data, headers=headers)
        return response

    def put_request(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, data=data)
        return response

if __name__ == '__main__':
    base_url = "http://127.0.0.1:8000/api/v1"

    api_client = ApiClient(base_url)

    get_response = api_client.get_request(endpoint="get-track-role/", )
    if get_response.status_code == 200:
        print("GET Request Successful:", get_response.text)
    else:
        print("GET Request Failed:", get_response.status_code, get_response.text)

   
