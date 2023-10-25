from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from pathlib import Path
from typing import Any

import pytest

from audible import utils as audible_utils
from audible.aescipher import AESCipher
from audible.localization import Locale


@pytest.mark.parametrize(
    "key,value,returns,expectation",
    [
        ("website_cookies", None, None, does_not_raise()),
        ("website_cookies", 1, None, pytest.raises(TypeError)),
        ("website_cookies", "1", None, pytest.raises(TypeError)),
        ("website_cookies", [1], None, pytest.raises(TypeError)),
        ("website_cookies", {"a": 1}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": 1.0}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": None}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": [1]}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": {"b": 1}}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": {"b": 1.0}}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": {"b": None}}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": {"b": [1]}}, None, pytest.raises(TypeError)),
        ("website_cookies", {"a": "1"}, {"a": "1"}, does_not_raise()),
        ("adp_token", None, None, does_not_raise()),
        ("adp_token", 1, None, pytest.raises(TypeError)),
        ("adp_token", "adp_token", None, pytest.raises(ValueError)),
        (
            "adp_token",
            "{enc:...}{key:...}{iv:...}{name:...}{serial:Mg==}",
            "{enc:...}{key:...}{iv:...}{name:...}{serial:Mg==}",
            does_not_raise(),
        ),
        ("access_token", None, None, does_not_raise()),
        ("access_token", 1, None, pytest.raises(TypeError)),
        ("access_token", "access_token", None, pytest.raises(ValueError)),
        ("access_token", "Atna|...", "Atna|...", does_not_raise()),
        ("refresh_token", None, None, does_not_raise()),
        ("refresh_token", 1, None, pytest.raises(TypeError)),
        ("refresh_token", "refresh_token", None, pytest.raises(ValueError)),
        ("refresh_token", "Atnr|...", "Atnr|...", does_not_raise()),
        ("device_private_key", None, None, does_not_raise()),
        ("device_private_key", 1, None, pytest.raises(TypeError)),
        ("device_private_key", "device_private_key", None, pytest.raises(ValueError)),
        (
            "device_private_key",
            "-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----\n",
            "-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----\n",
            does_not_raise(),
        ),
        ("expires", None, None, does_not_raise()),
        ("expires", {}, None, pytest.raises(TypeError)),
        ("expires", "12345+", None, pytest.raises(ValueError)),
        ("expires", "12345", 12345.0, does_not_raise()),
        ("expires", "12345.0", 12345.0, does_not_raise()),
        ("expires", 12345, 12345, does_not_raise()),
        ("expires", 12345.0, 12345.0, does_not_raise()),
        ("locale", None, None, does_not_raise()),
        ("locale", False, None, pytest.raises(TypeError)),
        ("locale", "us", Locale("us"), does_not_raise()),
        ("locale", "US", Locale("us"), does_not_raise()),
        ("locale", Locale("us"), Locale("us"), does_not_raise()),
        ("filename", None, None, does_not_raise()),
        ("filename", False, None, pytest.raises(TypeError)),
        ("filename", "credentials.json", Path("credentials.json"), does_not_raise()),
        (
            "filename",
            Path("credentials.json"),
            Path("credentials.json"),
            does_not_raise(),
        ),
        ("crypter", None, None, does_not_raise()),
        ("crypter", "credentials.json", None, pytest.raises(TypeError)),
        ("crypter", AESCipher("top_secret"), AESCipher("top_secret"), does_not_raise()),
        ("encryption", None, None, does_not_raise()),
        ("encryption", 1, None, pytest.raises(TypeError)),
        ("encryption", 0, None, pytest.raises(TypeError)),
        ("encryption", True, None, pytest.raises(ValueError)),
        ("encryption", False, False, does_not_raise()),
        ("encryption", "json", "json", does_not_raise()),
        ("encryption", "bytes", "bytes", does_not_raise()),
        ("unknown", "test", "test", does_not_raise()),
        ("unknown", 1, 1, does_not_raise()),
        ("unknown", 1.0, 1.0, does_not_raise()),
        ("unknown", None, None, does_not_raise()),
    ],
)
def test_convert(
    key: str,
    value: Any,
    returns: Any,
    expectation: AbstractContextManager[Exception | None],
) -> Any:
    with expectation:
        result = audible_utils.test_convert(key, value)
        assert result == returns


def test_elapsed_time() -> None:
    start = audible_utils.ElapsedTime()
    stop = start()
    assert isinstance(stop, float)
