#!/usr/bin/env python3
"""
Try alternative approaches to get process data from ifm AL1350
"""

import requests
import json


def test_alternative_formats(device_ip):
    """Test different request formats that might work"""
    base_url = f"http://{device_ip}"

    # Test 1: Try different content types
    print("🔍 Test 1: Different content types")

    payload = {
        "code": "request",
        "cid": 1,
        "adr": "/iolinkmaster/port[1]/iolinkdevice/pdin/getdata",
    }

    content_types = [
        "application/json",
        "application/x-www-form-urlencoded",
        "text/plain",
    ]

    for content_type in content_types:
        try:
            print(f"  📤 Trying content-type: {content_type}")
            if content_type == "application/x-www-form-urlencoded":
                response = requests.post(
                    base_url,
                    data=payload,
                    headers={"Content-Type": content_type},
                    timeout=5,
                )
            else:
                response = requests.post(
                    base_url,
                    json=payload,
                    headers={"Content-Type": content_type},
                    timeout=5,
                )

            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Response: {data}")
                if data.get("code") != 404:
                    print(f"  🎯 SUCCESS with {content_type}!")
                    return True

        except Exception as e:
            print(f"  ❌ Error: {e}")

    # Test 2: Try as GET request with query parameters
    print("\n🔍 Test 2: GET request with query parameters")
    try:
        params = {
            "code": "request",
            "cid": 1,
            "adr": "/iolinkmaster/port[1]/iolinkdevice/pdin/getdata",
        }
        response = requests.get(base_url, params=params, timeout=5)
        if response.status_code == 200:
            print(f"  ✅ GET Response: {response.text}")
    except Exception as e:
        print(f"  ❌ GET Error: {e}")

    # Test 3: Try direct endpoint access
    print("\n🔍 Test 3: Direct endpoint access")
    direct_endpoints = [
        "/iolinkmaster/port[1]/iolinkdevice/pdin/getdata",
        "/port[1]/iolinkdevice/pdin/getdata",
        "/data/port1",
        "/api/port1/data",
        "/pdi/port1",
    ]

    for endpoint in direct_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ Direct GET {endpoint}: {response.text}")
                if "404" not in response.text:
                    print(f"  🎯 SUCCESS with direct GET!")
                    return True
        except Exception as e:
            print(f"  ❌ Direct GET {endpoint} error: {e}")

    # Test 4: Try simple endpoint discovery
    print("\n🔍 Test 4: Simple endpoint discovery")
    simple_endpoints = ["/", "/api", "/data", "/status", "/info"]

    for endpoint in simple_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if (
                response.status_code == 200
                and "application/json" in response.headers.get("content-type", "")
            ):
                print(f"  ✅ JSON endpoint {endpoint}: {response.text}")
        except Exception as e:
            print(f"  ❌ Simple GET {endpoint} error: {e}")

    return False


def main():
    device_ip = "192.168.1.101"
    print(f"🔗 Testing alternative API approaches for {device_ip}")

    success = test_alternative_formats(device_ip)

    if not success:
        print("\n❌ No working API endpoints found")
        print("💡 Possible solutions:")
        print("   1. Device may not support REST API for process data")
        print("   2. API may be disabled or require configuration")
        print("   3. MQTT or other protocol may be required")
        print("   4. Web scraping may be the only option")
    else:
        print("\n✅ Found working API approach!")


if __name__ == "__main__":
    main()
