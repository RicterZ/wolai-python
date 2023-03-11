import requests

from wolai.logger import logger
from wolai.exceptions import WolaiRequestException


def request(url: str, data: dict = None, params: dict = None, method: str = 'post', headers: dict = None) -> dict:
    resp = getattr(requests, method)(url, json=data, params=params, headers=headers).json()
    logger.debug(f'http request: method={method} url={url} params={params} data={data}')
    if 'data' not in resp:
        if 'ErrorCode' in resp:
            raise WolaiRequestException(f'request failed with error code {resp["ErrorCode"]}: {resp["ErrorMessage"]}')
        elif 'error_code' in resp:
            raise WolaiRequestException(f'request failed with error code {resp["error_code"]}: {resp["message"]}')

    logger.debug(resp)
    return resp

