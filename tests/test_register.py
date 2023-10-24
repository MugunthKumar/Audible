import pytest
from pytest_httpx import HTTPXMock

from audible.localization import Locale
from audible.register import deregister


@pytest.mark.parametrize("with_username", [True, False])
@pytest.mark.parametrize("deregister_all", [True, False])
def test_deregister_success(
    register_response_success: HTTPXMock,
    all_locales: Locale,
    deregister_all: bool,
    with_username: bool
) -> None:
    """Test the deregister function."""
    access_token = "Atna|"
    domain = all_locales.domain
    target_domain = "audible" if with_username else "amazon"
    url = f"https://api.{target_domain}.{domain}/auth/deregister"

    assert deregister(
        access_token=access_token,
        domain=domain,
        deregister_all=deregister_all,
        with_username=with_username,
    ) == {"response": {"success": {}}, "request_id": "1234567890"}

    assert register_response_success.get_request(url=url) is not None

    assert register_response_success.get_request(
        match_json={"deregister_all_existing_accounts": deregister_all}
    ) is not None

    assert register_response_success.get_request(
        match_headers={"Authorization": f"Bearer {access_token}"}
    ) is not None


def test_deregister_fail(register_response_fail: HTTPXMock) -> None:
    """Test the deregister function."""
    with pytest.raises(Exception):
        deregister("Atna|", "com")
