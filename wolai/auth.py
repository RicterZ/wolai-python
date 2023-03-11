from wolai.constants import WOLAI_URL, API_VERSION_V1
from wolai.exceptions import WolaiTokenException
from wolai.common import request
from wolai.types.token import AppToken


WOLAI_TOKEN_API_URL = f'{WOLAI_URL}/{API_VERSION_V1}/token'


def get_token(app_id: str, app_secret: str) -> AppToken:
    data = {
        'appId': app_id,
        'appSecret': app_secret,
    }

    resp = request(WOLAI_TOKEN_API_URL, data=data)['data']
    if resp is None:
        raise WolaiTokenException('failed to get app token')

    return AppToken(**resp)


def refresh_token(token: AppToken) -> AppToken:
    # TODO: not work
    data = {
        'appId': token.app_id,
        'appToken': token.app_token
    }

    resp = request(WOLAI_TOKEN_API_URL, data=data, method='put')['data']
    if resp is None:
        raise WolaiTokenException('failed to refresh app token')

    return AppToken(**resp)


def get_authed_context(app_id: str, app_secret: str) -> callable:
    token = get_token(app_id, app_secret)
    headers = {'Authorization': token.app_token}

    def request_with_token(url: str, data: dict = None, params: dict = None, method: str = 'post') -> dict:
        return request(url, data=data, params=params, method=method, headers=headers)

    return request_with_token
