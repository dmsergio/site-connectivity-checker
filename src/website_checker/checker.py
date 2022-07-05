"""Module to check the website URL availability.

Examples:
    >>> from website_checker import checker
    >>> checker.site_is_online("pypi.org")
    True
    >>> checker.site_is_online("github.com")
    True

The module contains the following functions:

- `site_is_online(url)` - Returns `True` if website is online. Raise an
exception otherwise.
- `site_is_online_async(url)` - Returns `True` if website is online.
Raise an exception otherwise. This function has been called
asynchronously.
"""
import asyncio
from http.client import HTTPConnection
from typing import Optional
from urllib.parse import urlparse

import aiohttp


class ConnectionError(Exception):
    """Exception class to raise it by default when a connection has not
    been able.
    """


def site_is_online(url: str, timeout: Optional[int] = 2) -> bool:
    """Check if the target URL is online.

    Raise an exception otherwise.
    """
    error = ConnectionError("unknown error!")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout=timeout)
        try:
            connection.request("HEAD", "/")
            return True
        except Exception as exception:
            error = exception
        finally:
            connection.close()
    raise error


async def site_is_online_async(url: str, timeout: Optional[int] = 2) -> bool:
    """Check asynchronously if the target URL is online.

    Raise an exception otherwise.
    """
    error = ConnectionError("unknown error!")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for scheme in ("http", "https"):
        target_url = f"{scheme}://{host}"
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            except asyncio.exceptions.TimeoutError:
                error = Exception("time out")
            except Exception as exception:
                error = exception
    raise error
