"""Website Checker entrypoint."""
import asyncio
import pathlib
import sys
from argparse import Namespace
from typing import List

from website_checker.checker import site_is_online
from website_checker.checker import site_is_online_async
from website_checker.cli import display_check_result
from website_checker.cli import read_user_cli_args


def main():
    """Check the websites with the params set by the user on CLI."""
    user_args = read_user_cli_args()
    urls = _get_websites_urls(user_args)
    if not urls:
        print("Error: no URLs to check", file=sys.stderr)
        sys.exit(1)
    if user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)


def _get_websites_urls(user_args: Namespace) -> List:
    """Prepare a list with the URLs passed for the user in the CLI
    script."""
    urls = user_args.urls
    if user_args.input_file:
        urls += _read_urls_from_file(user_args.input_file)
    return urls


def _read_urls_from_file(file: str) -> List:
    """Returns a list with the URLs inside the file passed by
    argument. If the file not exists or it is empty, show a message
    for the user."""
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open() as urls_file:
            urls = [url.strip() for url in urls_file]
            if urls:
                return urls
            print(f"Error: empty input file, {file}", file=sys.stderr)
    else:
        print("Error: input file not found", file=sys.stderr)
    return []


def _synchronous_check(urls: List) -> None:
    """Check each URL if is online or doesn't, and show a info message
    to the user."""
    for url in urls:
        error = ""
        try:
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)


async def _asynchronous_check(urls: List):
    """Check each URL if is online or doesn't, and show a info message
    to the user. This process is executed asynchronously."""

    async def _check(url):
        error = ""
        try:
            result = await site_is_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)

    await asyncio.gather(*(_check(url) for url in urls))


if __name__ == "__main__":
    main()
