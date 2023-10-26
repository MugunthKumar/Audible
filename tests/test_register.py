from typing import Any
from unittest.mock import ANY

import pytest
from pytest_httpx import HTTPXMock

from audible.localization import Locale
from audible.register import deregister, register


@pytest.mark.parametrize("with_username", [True, False])
def test_register_success(
    register_response_success_data: dict[str, Any],
    httpx_mock: HTTPXMock,
    with_username: bool,
    all_locales: Locale,
) -> None:
    httpx_request = register_response_success_data["request"]
    httpx_response = register_response_success_data["response"]

    ac = httpx_request["json"]["auth_data"]["authorization_code"]
    cv = httpx_request["json"]["auth_data"]["code_verifier"].encode()
    domain = all_locales.domain
    target_domain = "audible" if with_username else "amazon"
    url = f"https://api.{target_domain}.{domain}/auth/register"
    httpx_request["json"]["cookies"]["domain"] = f".amazon.{domain}"
    serial = httpx_request["json"]["registration_data"]["device_serial"]

    httpx_mock.add_response(
        method=httpx_request["method"],
        url=url,
        match_json=httpx_request["json"],
        json=httpx_response["json"],
    )

    reg_resp = register(
        authorization_code=ac,
        code_verifier=cv,
        domain=domain,
        serial=serial,
        with_username=with_username,
    )
    # req = httpx_mock.get_request(url=re.compile("https://api.*/auth/register"))

    json_response = httpx_response["json"]["response"]["success"]
    tokens = json_response["tokens"]
    extensions = json_response["extensions"]
    assert tokens["mac_dms"]["adp_token"] == reg_resp["adp_token"]
    assert tokens["mac_dms"]["device_private_key"] == reg_resp["device_private_key"]
    assert tokens["bearer"]["access_token"] == reg_resp["access_token"]
    assert tokens["bearer"]["refresh_token"] == reg_resp["refresh_token"]
    assert extensions["device_info"] == reg_resp["device_info"]
    assert extensions["customer_info"] == reg_resp["customer_info"]


def test_register_fail(
    register_response_fail_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    httpx_response = register_response_fail_data["response"]

    httpx_mock.add_response(status_code=httpx_response["status_code"])
    with pytest.raises(Exception):
        register(
            "...",
            b"...",
            "com",
            "...",
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

    at = "..."
    domain = all_locales.domain
    target_domain = "audible" if with_username else "amazon"
    url = f"https://api.{target_domain}.{domain}/auth/deregister"
    httpx_request["json"]["deregister_all_existing_accounts"] = deregister_all

    httpx_mock.add_response(
        method=httpx_request["method"],
        url=url,
        match_json=httpx_request["json"],
        json=httpx_response["json"],
    )

    dereg_resp = deregister(
        access_token=at,
        domain=domain,
        deregister_all=deregister_all,
        with_username=with_username,
    )

    assert dereg_resp == httpx_response["json"]
    assert httpx_mock.get_requests()[0].headers["Authorization"] == f"Bearer {at}"


def test_deregister_fail(
    deregister_response_fail_data: dict[str, Any],
    httpx_mock: HTTPXMock,
) -> None:
    """Test the deregister function."""
    httpx_response = deregister_response_fail_data["response"]

    httpx_mock.add_response(status_code=httpx_response["status_code"])
    with pytest.raises(Exception):
        deregister("...", "com")
