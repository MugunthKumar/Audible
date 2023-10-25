from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from audible.localization import Locale
from audible.register import deregister, register


def test_register_success(
    register_response_success_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    httpx_request = register_response_success_data["request"]
    httpx_response = register_response_success_data["response"]

    httpx_mock.add_response(
        method=httpx_request["method"],
        json=httpx_response["json"],
    )

    ac = "test_authorization_code"
    cv = b"test_code_verifier"
    domain = "com"
    serial = "865DF703EF0F4A638998F7A1A49E5AB2"
    resp = register(
        authorization_code=ac, code_verifier=cv, domain=domain, serial=serial
    )
    # req = httpx_mock.get_request(url=re.compile("https://api.*/auth/register"))

    assert (
        resp["customer_info"]["user_id"] == "amzn1.account.HLP4WSECFFXS2KQVPVSY3I0MQAOR"
    )


def test_register_fail(
    register_response_fail_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    httpx_response = register_response_fail_data["response"]

    httpx_mock.add_response(
        status_code=httpx_response["status_code"],
        json=httpx_response["json"],
    )
    with pytest.raises(Exception):
        register(
            "test_authorization_code",
            b"test_code_verifier",
            "com",
            "865DF703EF0F4A638998F7A1A49E5AB2",
        )


@pytest.mark.parametrize("with_username", [True, False])
@pytest.mark.parametrize("deregister_all", [True, False])
def test_deregister_success(
    deregister_response_success_data: dict[str, Any],
    httpx_mock: HTTPXMock,
    all_locales: Locale,
    deregister_all: bool,
    with_username: bool,
) -> None:
    """Test the deregister function."""
    httpx_request = deregister_response_success_data["request"]
    httpx_response = deregister_response_success_data["response"]

    httpx_mock.add_response(
        method=httpx_request["method"],
        json=httpx_response["json"],
    )

    at = "Atna|"
    domain = all_locales.domain
    target_domain = "audible" if with_username else "amazon"
    url = f"https://api.{target_domain}.{domain}/auth/deregister"

    assert (
        deregister(
            access_token=at,
            domain=domain,
            deregister_all=deregister_all,
            with_username=with_username,
        )
        == httpx_response["json"]
    )

    assert httpx_mock.get_request(url=url) is not None

    assert (
        httpx_mock.get_request(
            match_json={"deregister_all_existing_accounts": deregister_all}
        )
        is not None
    )

    assert (
        httpx_mock.get_request(match_headers={"Authorization": f"Bearer {at}"})
        is not None
    )


def test_deregister_fail(
    deregister_response_fail_data: dict[str, Any],
    httpx_mock: HTTPXMock,
) -> None:
    """Test the deregister function."""
    httpx_request = deregister_response_fail_data["request"]
    httpx_response = deregister_response_fail_data["response"]

    httpx_mock.add_response(
        method=httpx_request["method"],
        status_code=httpx_response["status_code"],
        json=httpx_response["json"],
    )
    with pytest.raises(Exception):
        deregister("Atna|", "com")
