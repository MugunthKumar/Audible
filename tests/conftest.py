import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from audible.localization import LOCALE_TEMPLATES, Locale


BASE_PATH = Path.cwd().joinpath("tests", "data")


def get_file_with_json_extension(file_name: str) -> Path:
    if not file_name.endswith(".json"):
        file_name += ".json"
    return BASE_PATH.joinpath(file_name)


def read_file(file_name: str) -> Any:
    file_path = get_file_with_json_extension(file_name)
    with file_path.open("r") as f:
        return json.load(f)


AVAILABLE_COUNTRY_CODES = [
    market["country_code"] for market in LOCALE_TEMPLATES.values()
]


@pytest.fixture(scope="session", params=AVAILABLE_COUNTRY_CODES)
def all_locales(request: pytest.FixtureRequest) -> Locale:
    country_code: str = request.param
    return Locale(country_code=country_code)


@pytest.fixture
def register_response_success_data() -> Iterator[dict[str, Any]]:
    yield read_file("register_success")


@pytest.fixture
def register_response_fail_data() -> Iterator[dict[str, Any]]:
    yield read_file("register_fail")


@pytest.fixture
def deregister_response_success_data() -> Iterator[dict[str, Any]]:
    yield read_file("deregister_success")


@pytest.fixture
def deregister_response_fail_data() -> Iterator[dict[str, Any]]:
    yield read_file("deregister_fail")
