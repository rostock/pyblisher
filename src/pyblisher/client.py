from pyblisher.response import ExtResponse
from .settings import settings
from .bearerAuth import BearerAuth
from httpx import request, Client, Response

class Client:
    def __init__(self):
        self.__project_id = settings.VCP_API_PROJECT_ID
        self.__data_path = '/vcs/data/public/'  # im root System unter /nfs/daten/rostock3d/vcpublisher
        self.__epsg = '25833'
        self.__connected = False


    def __login__(self) -> bool:
        """
        Login to API
        :return: bearer token
        """
        if not self.__connected:
            bearer: str = 'no bearer'
            self.__url: str = settings.HOST
            if self.__url:
                response = ExtResponse(request(
                    method='POST',
                    url=f'{self.__url}/login/',
                    auth=(settings.USER, settings.PASSWORD),
                    headers={
                        'Content-Type': 'application/json'
                    }
                ))
                if response.ok:
                    bearer: str = response.json()['token']
                    self.__session = Client()
                    self.__session.auth = BearerAuth(bearer)
                    self.__connected = True
                else:
                    raise Exception(f'Login failed: {response.__dict__}')
        return self.__connected
