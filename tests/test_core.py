from unittest.mock import patch

from ntmn import __version__
from ntmn.core import ping_target


def test_version() -> None:
    assert __version__ is not None


async def test_ping_target() -> None:
    with patch('ntmn.core.ping', return_value=(1234567890, 20, True)):
        timestamp, latency, status = ping_target("example.com")
        assert timestamp == 1234567890
        assert latency == 20
        assert status is True
