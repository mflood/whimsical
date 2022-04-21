"""

    data.py
    download aoc data

Create config/flood.yml:

aoc_client:
    cookies: 
        _ga: "GA1.2.111111111.1111111111"
        session: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        _gid: "GA1.2.111111111.1111111111" 
        _gat: "1"
    user_agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
    authority: "adventofcode.com"

"""
from dataclasses import dataclass
import requests
import datetime
import os
from flood_advent.utils import init_logging
from flood_advent.utils import LOGGER_NAME
import logging
import argparse

import sys
import yaml

DATA_ROOT = "./data"
AOC_API = "https://adventofcode.com"


@dataclass
class Headers:
    cookies: dict
    user_agent: str
    authority: str

    def get_dict(self):

        pairs = [f"{k}={v}" for k, v in self.cookies.items()]
        cookie_string = "; ".join(pairs)
        return {
            "cookie": cookie_string,
            "user-agent": self.user_agent,
            "authority": self.authority,
        }


def get_data(year: str, day: str, headers: Headers) -> str:

    full_path = f"{AOC_API}/{year}/day/{day}/input"
    print(f"downloading from {full_path}")
    response = requests.get(full_path, headers=headers.get_dict())
    return response.content.decode()


def save_data(filepath: str, data: str) -> None:
    print(f"writing {len(data)} bytes to {filepath}")
    with open(filepath, "w") as handle:
        handle.write(data)


def get_output_folder_path(year: str, day: str):
    return os.path.join(DATA_ROOT.rstrip("/"), str(year), "day", str(day))


def make_output_folder(folderpath: str) -> None:
    print(f"Creating folder {folderpath}")
    try:
        os.makedirs(folderpath)
    except FileExistsError:
        pass


def download_and_save_data(year: str, day: str, headers: Headers):

    folderpath = get_output_folder_path(year=year, day=day)

    if not os.path.exists(folderpath):
        make_output_folder(folderpath)

    filepath = os.path.join(folderpath, "input.txt")

    if os.path.exists(filepath):
        print(f"data file already exists for {year} {day}: {filepath}")
        return

    data = get_data(year=year, day=day, headers=headers)
    save_data(filepath=filepath, data=data)

def create_test_input_file(year: str, day: str):
    folderpath = get_output_folder_path(year=year, day=day)
    filepath = os.path.join(folderpath, "test-input.txt")
    if os.path.exists(filepath):
        print(f"test file {filepath} already exists")
    else:
        print(f"creating test file {filepath}")
        with open(filepath, "w") as handle:
            handle.write("")


def dump_data(year: str, day: str):
    folderpath = get_output_folder_path(year=year, day=day)
    filepath = os.path.join(folderpath, "input.txt")
    with open(filepath, "r") as handle:
        for line in handle:
            print(line.strip())


def get_current_year_day():
    now = datetime.datetime.now()
    year = now.year
    day = now.day
    hour = now.hour
    if hour >= 22:
        day += 1
    return f"{year}", f"{day}"


def parse_args(argv=None):
    """
        Parse command line args
    """
    parser = argparse.ArgumentParser(description="Main Driver for Frivenmeld")

    parser.add_argument('-v',
                        action="store_true",
                        dest="verbose",
                        required=False,
                        help="Debug output")

    parser.add_argument("-y",
                        dest="year",
                        help="Use this YYYY year instead of current year")

    parser.add_argument("-d",
                        dest="day",
                        help="Use this D day instead of current day")

    results = parser.parse_args(argv)
    return results 


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    handle = open("config/flood.yml", "r")
    data = handle.read()
    handle.close()
    as_dict = yaml.safe_load(data)

    headers = Headers(
        cookies=as_dict["aoc_client"]["cookies"],
        user_agent=as_dict["aoc_client"]["user_agent"],
        authority=as_dict["aoc_client"]["authority"],
    )

    year, day = get_current_year_day()

    if args.year:
        year = args.year

    if args.day:
        day  = args.day

    download_and_save_data(year=year, day=day, headers=headers)
    dump_data(year=year, day=day)
    create_test_input_file(year=year, day=day)

# end
