import requests
from enum import Enum


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class ApiRequest:
    def __init__(self, endpoint: str, data: dict, method: RequestMethod):
        self.endpoint = endpoint
        self.data = data
        self.method = method

    def send(self):
        if self.method == RequestMethod.GET:
            response = requests.get(self.endpoint, params=self.data)
        elif self.method == RequestMethod.POST:
            response = requests.post(self.endpoint, json=self.data)
        elif self.method == RequestMethod.PUT:
            response = requests.put(self.endpoint, json=self.data)
        elif self.method == RequestMethod.DELETE:
            response = requests.delete(self.endpoint, json=self.data)
        else:
            raise ValueError("Unsupported HTTP method")

        return response


class LoggerDecorator:
    def __init__(self, api_request: ApiRequest):
        self.api_request = api_request

    def send(self):
        print(
            f"Sending {self.api_request.method.value} request to {self.api_request.endpoint}"
        )
        print(f"Data: {self.api_request.data}")
        response = self.api_request.send()
        print(f"Response: {response.status_code}")
        return response
