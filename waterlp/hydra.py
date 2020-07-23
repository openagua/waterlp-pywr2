import requests
import json
from attrdict import AttrDict
from os import environ


class Hydra(object):
    """
    Example:

    # Set up the class
    hydra = Hydra('https://www.openagua.org/hydra', api_key=os.environ['OPENAGUA_SECRET_KEY'])

    # Method 1: hydra.call(function, **kwargs)
    resp1 = hydra.call('get_project', project_id=123)

    # Method 2: hydra.func_name(**kwargs)
    resp2 = hydra.get_project(project_id=123)

    """

    endpoint = environ.get('OPENAGUA_HYDRA_ENDPOINT', 'https://www.openagua.org/hydra/')
    api_key = environ.get('OPENAGUA_SECRET_KEY')

    username = None
    password = None

    def __init__(self, endpoint=None, username='', password=None, api_key=None):

        endpoint = endpoint or self.endpoint

        if endpoint and endpoint[-1] != '/':
            endpoint += '/'

        self.endpoint = endpoint

        self.username = username or self.username
        self.password = password or api_key or self.api_key

    def call(self, func, dict_kwargs=None, **kwargs):
        if dict_kwargs is not None:
            return self._call(func, **dict_kwargs)
        else:
            return self._call(func, **kwargs)

    def _call(self, func, *args, **kwargs):
        payload = {}
        if args:
            payload['args'] = list(args)
            payload['kwargs'] = kwargs
        else:
            payload = kwargs
        endpoint = self.endpoint + func
        resp = requests.post(endpoint, auth=(self.username, self.password), json=payload)
        try:
            json_resp = json.loads(resp.content.decode())
            return AttrDict(json_resp)
        except:
            return resp.content.decode()

    def __getattr__(self, name):
        def method(*args, **kwargs):
            if name == 'call':
                return self._call(*args, **kwargs)
            else:
                return self._call(name, *args, **kwargs)

        return method
