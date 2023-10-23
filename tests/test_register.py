from unittest.mock import Mock

import httpx
import pytest

from audible.register import deregister


@pytest.mark.parametrize(
    "domain, deregister_all, with_username, url",
    [
        ("com", True, True, "https://api.audible.com/auth/deregister"),
        ("com", True, False, "https://api.amazon.com/auth/deregister"),
        ("com", False, True, "https://api.audible.com/auth/deregister"),
        ("com", False, False, "https://api.amazon.com/auth/deregister"),
        ("co.uk", True, True, "https://api.audible.co.uk/auth/deregister"),
        ("co.uk", True, False, "https://api.amazon.co.uk/auth/deregister"),
        ("co.uk", False, True, "https://api.audible.co.uk/auth/deregister"),
        ("co.uk", False, False, "https://api.amazon.co.uk/auth/deregister"),
    ],
)
def test_deregister_success(
    mocker: Mock, domain: str, deregister_all: bool, with_username: bool, url: str
) -> None:
    """Test the deregister function."""
    request_mock = mocker.patch(
        "audible.register.httpx.post",
        return_value=httpx.Response(200, json={"status": "ok"}),
    )
    assert deregister(
        "Atna|",
        domain=domain,
        deregister_all=deregister_all,
        with_username=with_username,
    ) == {"status": "ok"}
    request_mock.assert_called_with(
        url,
        json={"deregister_all_existing_accounts": deregister_all},
        headers={"Authorization": "Bearer Atna|"},
    )


def test_deregister_fail(mocker: Mock) -> None:
    """Test the deregister function."""
    mocker.patch(
        "audible.register.httpx.post",
        return_value=httpx.Response(403, json={"status": "forbidden"}),
    )
    with pytest.raises(Exception):
        deregister("Atna|", "com")
