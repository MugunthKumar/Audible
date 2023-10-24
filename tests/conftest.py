import pytest
from pytest_httpx import HTTPXMock

from audible.localization import LOCALE_TEMPLATES, Locale


AVAILABLE_COUNTRY_CODES = [
    market["country_code"] for market in LOCALE_TEMPLATES.values()
]


@pytest.fixture(scope="session", params=AVAILABLE_COUNTRY_CODES)
def all_locales(request: pytest.FixtureRequest) -> Locale:
    country_code: str = request.param
    return Locale(country_code=country_code)


@pytest.fixture
def register_response_success(httpx_mock: HTTPXMock) -> HTTPXMock:
    httpx_mock.add_response(
        method="POST",
        json={"response": {"success": {}}, "request_id": "1234567890"},
    )
    return httpx_mock


@pytest.fixture
def register_response_fail(httpx_mock: HTTPXMock) -> HTTPXMock:
    httpx_mock.add_response(
        status_code=403,
        method="POST",
        json={
            "response": {
                "error": {
                    "code": "InvalidToken",
                    "message": "One or more tokens are invalid."
                }
            },
            "request_id": "1234567890"
        },
    )
    return httpx_mock
