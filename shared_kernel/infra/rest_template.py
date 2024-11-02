from shared_kernel.infra.logger import logger
import requests

def get(url, isThrowable: bool = False, isExpectingResult: bool = True):
    try:
        logger.info('Making request to: '+ url)
        r = requests.get(url)
        if isThrowable:
            r.raise_for_status()
        if isExpectingResult:
            return r.json()
    except requests.RequestException as e:
        logger.error(e)
        #raise RuntimeError(f"Failed to making request {url} with error: {e}")

def post(url, data: dict= None, isThrowable: bool = False):
    try:
        logger.info('Making request to: '+ url)
        r = requests.post(url, json=data)
        if isThrowable:
            r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        # Handle request error here
        logger.error(e)
        #raise RuntimeError(f"Failed to making request {url} with error: {e}")