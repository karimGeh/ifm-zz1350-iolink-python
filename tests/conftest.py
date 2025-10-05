"""
Configuration file for pytest
"""

import pytest

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires hardware)"
    )