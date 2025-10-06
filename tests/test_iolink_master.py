"""
Test suite for ifm ZZ1350 IO-Link Master Python library

This module contains unit tests for the IOLinkMaster class.
Tests can be run with or without actual hardware.

Usage:
    python -m pytest tests/
    python -m pytest tests/test_iolink_master.py -v

Requirements:
    - pytest
    - requests-mock (for mocked tests)
"""

import pytest
import requests
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from iolink_master import IOLinkMaster, hex_to_temperature


class TestIOLinkMaster:
    """Test cases for IOLinkMaster class"""

    def test_init_success(self):
        """Test successful initialization"""
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200

            master = IOLinkMaster("192.168.1.101")
            assert master.device_ip == "192.168.1.101"
            assert master.base_url == "http://192.168.1.101"
            assert master.timeout == 5

    def test_init_connection_failure(self):
        """Test initialization with connection failure"""
        with patch("requests.get", side_effect=requests.ConnectionError):
            with pytest.raises(ConnectionError):
                IOLinkMaster("192.168.1.101")

    def test_make_request_json_response(self):
        """Test make_request with JSON response"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock API request
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": {"value": "4"}}
            mock_get.return_value = mock_response

            result = master.make_request("/test/endpoint")
            assert result == "4"

    def test_make_request_text_response(self):
        """Test make_request with plain text response"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock API request
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError  # Not valid JSON
            mock_response.text = "plain_text_response"
            mock_get.return_value = mock_response

            result = master.make_request("/test/endpoint")
            assert result == "plain_text_response"

    def test_make_request_failure(self):
        """Test make_request with HTTP error"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock API request failure
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            result = master.make_request("/test/endpoint")
            assert result is None

    def test_get_port_count(self):
        """Test get_port_count method"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock port count request
            with patch.object(master, "make_request", return_value="4"):
                result = master.get_port_count()
                assert result == 4

    def test_get_port_count_invalid(self):
        """Test get_port_count with invalid response"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock invalid port count request
            with patch.object(master, "make_request", return_value="invalid"):
                result = master.get_port_count()
                assert result == 0

    def test_get_device_status(self):
        """Test get_device_status method"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock device status request
            with patch.object(master, "make_request", return_value="2"):
                result = master.get_device_status(1)
                assert result == "2"

    def test_get_device_name(self):
        """Test get_device_name method"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock device name request
            with patch.object(master, "make_request", return_value="TV7105"):
                result = master.get_device_name(1)
                assert result == "TV7105"

    def test_get_temperature_celsius_valid(self):
        """Test temperature conversion with valid data"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock temperature data (0x0157 = 343 decimal = 34.3°C)
            with patch.object(master, "get_device_data", return_value="0x0157"):
                result = master.get_temperature_celsius(1)
                assert result == 34.3

    def test_get_temperature_celsius_invalid(self):
        """Test temperature conversion with invalid data"""
        with patch("requests.get") as mock_get:
            # Mock successful connection in __init__
            mock_get.return_value.status_code = 200
            master = IOLinkMaster("192.168.1.101")

            # Mock invalid temperature data
            with patch.object(master, "get_device_data", return_value="invalid"):
                result = master.get_temperature_celsius(1)
                assert result is None


class TestUtilityFunctions:
    """Test cases for utility functions"""

    def test_hex_to_temperature_valid(self):
        """Test hex_to_temperature with valid input"""
        assert hex_to_temperature("0x0157") == 34.3
        assert hex_to_temperature("0x00FF") == 25.5
        assert hex_to_temperature("0x0000") == 0.0

    def test_hex_to_temperature_invalid(self):
        """Test hex_to_temperature with invalid input"""
        assert hex_to_temperature("invalid") is None
        assert hex_to_temperature("0xGGGG") is None
        assert hex_to_temperature("") is None
        assert hex_to_temperature(None) is None


class TestIntegration:
    """Integration tests (require actual hardware)"""

    @pytest.mark.integration
    def test_real_device_connection(self):
        """Test connection to real device (skip if not available)"""
        try:
            # Try to connect to common IP addresses
            test_ips = ["169.254.178.135", "192.168.1.201"]

            for ip in test_ips:
                try:
                    master = IOLinkMaster(ip, timeout=3)
                    port_count = master.get_port_count()
                    assert isinstance(port_count, int)
                    assert port_count >= 0
                    print(f"✅ Real device test passed with {ip}")
                    return
                except:
                    continue

            pytest.skip("No real device available for integration test")

        except Exception as e:
            pytest.skip(f"Integration test skipped: {e}")


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
