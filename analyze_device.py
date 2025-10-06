#!/usr/bin/env python3
"""
Analyze the ifm AL1350 web interface to understand available endpoints
"""

import requests
import re


def analyze_web_interface(url):
    """Analyze the web interface HTML for clues about API endpoints"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ Web interface accessible")
            print(f"📄 Content length: {len(response.text)} characters")

            # Look for JavaScript that might reveal API endpoints
            js_patterns = [
                r'fetch\s*\(\s*["\']([^"\']+)["\']',
                r'XMLHttpRequest.*?open\s*\(\s*["\'][^"\']*["\'],\s*["\']([^"\']+)["\']',
                r'ajax\s*\(\s*["\']([^"\']+)["\']',
                r'/api/[^"\'>\s]+',
                r'/iolinkmaster/[^"\'>\s]+',
                r'href\s*=\s*["\']([^"\']*api[^"\']*)["\']',
                r'action\s*=\s*["\']([^"\']*)["\']',
            ]

            content = response.text
            print(f"\n🔍 Searching for API endpoints in HTML...")

            for pattern in js_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"📍 Pattern '{pattern}' found:")
                    for match in matches:
                        print(f"   {match}")

            # Look for any references to endpoints
            endpoint_keywords = [
                "iolinkmaster",
                "api",
                "data",
                "port",
                "sensor",
                "temperature",
            ]
            for keyword in endpoint_keywords:
                if keyword in content.lower():
                    print(f"🔑 Found keyword '{keyword}' in HTML")

            # Print first 500 chars to see structure
            print(f"\n📝 HTML sample (first 500 chars):")
            print(content[:500])

            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_mqtt_or_websocket(device_ip):
    """Check if device supports MQTT or WebSocket connections"""
    import socket

    mqtt_port = 1883
    websocket_port = 80

    print(f"\n🔍 Testing MQTT connection on port {mqtt_port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((device_ip, mqtt_port))
        sock.close()

        if result == 0:
            print(f"✅ MQTT port {mqtt_port} is open")
        else:
            print(f"❌ MQTT port {mqtt_port} is closed")
    except Exception as e:
        print(f"❌ MQTT test failed: {e}")


def main():
    device_ip = "192.168.1.101"
    base_url = f"http://{device_ip}"

    print(f"🔗 Analyzing ifm AL1350 at {device_ip}")

    # Analyze web interface
    analyze_web_interface(base_url)

    # Test MQTT
    test_mqtt_or_websocket(device_ip)


if __name__ == "__main__":
    main()
