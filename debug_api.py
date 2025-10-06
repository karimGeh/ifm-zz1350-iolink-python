#!/usr/bin/env python3
"""
Debug script to test ifm AL1350 API endpoints
"""

import requests
import json


def test_endpoint(url, endpoint, cid=1):
    """Test a specific API endpoint"""
    payload = {"code": "request", "cid": cid, "adr": endpoint}

    try:
        print(f"\n🔍 Testing endpoint: {endpoint}")
        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}, timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data}")
            return data
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None


def main():
    device_ip = "192.168.1.101"
    base_url = f"http://{device_ip}"

    print(f"🔗 Testing API endpoints for {device_ip}")

    # Test various endpoint variations
    endpoints_to_test = [
        "/iolinkmaster/port/numberofports/getdata",
        "/port/numberofports/getdata",
        "/iolinkmaster/numberofports/getdata",
        "/numberofports/getdata",
        "/api/iolinkmaster/port/numberofports/getdata",
        "/getdata/iolinkmaster/port/numberofports",
        "/iolinkmaster/port/count",
        "/iolinkmaster/ports",
        "/iolinkmaster/info",
        "/iolinkmaster/status",
        "/iolinkmaster",
        "/api",
        "/info",
        "/status",
    ]

    for endpoint in endpoints_to_test:
        result = test_endpoint(base_url, endpoint)
        if result and result.get("code") != 404:
            print(f"🎯 WORKING ENDPOINT FOUND: {endpoint}")


if __name__ == "__main__":
    main()
