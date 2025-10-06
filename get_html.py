#!/usr/bin/env python3
"""
Get full HTML content from ifm AL1350 to understand data structure
"""

import requests
import re


def get_full_html_content(url):
    """Get and analyze the complete HTML content"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            content = response.text
            print(f"✅ Full HTML content retrieved ({len(content)} chars)")
            print("=" * 80)
            print(content)
            print("=" * 80)

            # Look for any data patterns
            print("\n🔍 Looking for data patterns...")

            # Look for temperature values
            temp_patterns = [
                r"(\d+\.?\d*)\s*°C",
                r"temperature[:\s]*(\d+\.?\d*)",
                r"temp[:\s]*(\d+\.?\d*)",
                r"(\d+\.?\d*)\s*celsius",
            ]

            for pattern in temp_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"🌡️ Temperature values found: {matches}")

            # Look for port information
            port_patterns = [r"port\s*(\d+)", r"Port\s*(\d+)", r"PORT\s*(\d+)"]

            for pattern in port_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"🔌 Port numbers found: {matches}")

            # Look for hex data
            hex_patterns = [r"0x[0-9a-fA-F]+", r"[0-9a-fA-F]{4,8}"]

            for pattern in hex_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    print(f"🔢 Hex values found: {matches}")

            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    device_ip = "192.168.1.101"
    base_url = f"http://{device_ip}"

    print(f"🔗 Getting full HTML from ifm AL1350 at {device_ip}")
    get_full_html_content(base_url)


if __name__ == "__main__":
    main()
