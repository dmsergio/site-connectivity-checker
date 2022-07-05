"""CLI with the options available for the user. """
import argparse


def read_user_cli_args():
    """CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="website_checker",
        description="check the availability of websites",
    )
    parser.add_argument(
        "-u",
        "--urls",
        metavar="URLs",
        nargs="+",
        type=str,
        default=[],
        help="enter one or more websites URLs",
    )
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="read URLs from a file",
    )
    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="run the connectivity check asynchronously",
    )
    return parser.parse_args()


def display_check_result(result: bool, url: str, error: str) -> None:
    """Display to the user the website URL status."""
    print(f"The status of '{url}' is:", end=" ")
    if result:
        print("'Online!' 👍")
    else:
        print(f"'Offline?' 👎\nError: '{error}'")
