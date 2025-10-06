"""
ifm ZZ1350 IO-Link Master Python Library

A Python library for communicating with the ifm AL1350 IO-Link Master.
"""

from .iolink_master import IOLinkMaster, hex_to_temperature

__version__ = "1.0.0"
__author__ = "Karim Saadeldin"
__email__ = "karim2jihad@gmail.com"

__all__ = ["IOLinkMaster", "hex_to_temperature"]
