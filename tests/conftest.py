"""Pytest configuration and fixtures"""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_psutil_cpu():
    """Mock psutil CPU functions"""
    with patch("psutil.cpu_percent", return_value=45.5) as mock_percent, \
         patch("psutil.cpu_count", return_value=8) as mock_count, \
         patch("psutil.cpu_freq") as mock_freq:
        mock_freq.return_value = MagicMock(
            current=2400.0,
            min=800.0,
            max=3200.0,
            _asdict=lambda: {"current": 2400.0, "min": 800.0, "max": 3200.0}
        )
        yield {
            "percent": mock_percent,
            "count": mock_count,
            "freq": mock_freq,
        }


@pytest.fixture
def mock_psutil_memory():
    """Mock psutil memory functions"""
    with patch("psutil.virtual_memory") as mock:
        mock.return_value = MagicMock(
            percent=65.2,
            total=17179869184,  # 16 GB
            available=6012954624,  # ~5.6 GB
            used=11166914560,  # ~10.4 GB
        )
        yield mock


@pytest.fixture
def mock_psutil_disk():
    """Mock psutil disk functions"""
    with patch("psutil.disk_usage") as mock:
        mock.return_value = MagicMock(
            percent=72.3,
            total=500107862016,  # ~465 GB
            used=361578151936,  # ~337 GB
            free=138529710080,  # ~129 GB
        )
        yield mock


@pytest.fixture
def mock_psutil_network():
    """Mock psutil network functions"""
    with patch("psutil.net_io_counters") as mock:
        mock.return_value = MagicMock(
            bytes_sent=1048576000,  # ~1000 MB
            bytes_recv=2097152000,  # ~2000 MB
            packets_sent=1000000,
            packets_recv=2000000,
            errin=10,
            errout=5,
        )
        yield mock


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    with patch("openai.OpenAI") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def mock_pyaudio():
    """Mock PyAudio"""
    with patch("pyaudio.PyAudio") as mock:
        audio = MagicMock()
        stream = MagicMock()
        stream.read.return_value = b"\x00" * 1024
        audio.open.return_value = stream
        audio.get_sample_size.return_value = 2
        mock.return_value = audio
        yield {"pyaudio": mock, "audio": audio, "stream": stream}
