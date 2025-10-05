"""
Network Discovery Script for ifm IO-Link Master

This script helps you find your IO-Link Master on the network using the
ARP (Address Resolution Protocol) method described in the LinkedIn article.

Usage:
    python network_discovery.py

Features:
    - ARP table scanning for ifm devices
    - MAC address verification
    - Network interface detection
    - Connection testing

Requirements:
    - Windows: arp command (built-in)
    - Linux/Mac: arp command (usually pre-installed)
"""

import subprocess
import re
import sys
import os
import requests
from typing import List, Dict, Optional

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


def run_arp_command() -> str:
    """
    Execute the ARP command and return the output

    Returns:
        str: ARP command output
    """
    try:
        if sys.platform.startswith("win"):
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        else:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout
        else:
            print(f"❌ ARP command failed: {result.stderr}")
            return ""
    except FileNotFoundError:
        print("❌ ARP command not found. Please ensure it's installed.")
        return ""


def parse_arp_output(arp_output: str) -> List[Dict[str, str]]:
    """
    Parse ARP command output to extract device information

    Args:
        arp_output (str): Raw ARP command output

    Returns:
        List[Dict]: List of devices with IP and MAC addresses
    """
    devices = []

    # Regex pattern to match IP and MAC addresses
    # Supports both Windows and Unix format
    pattern = r"(\d+\.\d+\.\d+\.\d+)\s+.*?([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})"

    matches = re.findall(pattern, arp_output)

    for ip, mac in matches:
        # Normalize MAC address format
        mac_normalized = mac.replace("-", ":").upper()
        devices.append({"ip": ip, "mac": mac_normalized, "mac_raw": mac})

    return devices


def is_ifm_device(mac_address: str) -> bool:
    """
    Check if MAC address belongs to an ifm device

    ifm electronic uses OUI (Organizationally Unique Identifier) ranges.
    Common ifm OUI prefixes: 00:02:01, 00:30:26

    Args:
        mac_address (str): MAC address to check

    Returns:
        bool: True if likely an ifm device
    """
    mac_upper = mac_address.upper()

    # Known ifm OUI prefixes
    ifm_prefixes = [
        "00:02:01",  # Common ifm prefix
        "00:30:26",  # Another ifm prefix
    ]

    for prefix in ifm_prefixes:
        if mac_upper.startswith(prefix):
            return True

    return False


def test_iolink_connection(ip_address: str) -> bool:
    """
    Test if the device at the given IP is an IO-Link Master

    Args:
        ip_address (str): IP address to test

    Returns:
        bool: True if device responds like an IO-Link Master
    """
    try:
        # Test basic HTTP connection
        response = requests.get(f"http://{ip_address}", timeout=3)

        # Check if response looks like ifm device
        if response.status_code == 200:
            content = response.text.lower()
            if "ifm" in content or "iolink" in content or "al1350" in content:
                return True
    except requests.RequestException:
        pass

    return False


def discover_iolink_master() -> Optional[str]:
    """
    Main discovery function to find IO-Link Master on network

    Returns:
        str: IP address of discovered IO-Link Master, None if not found
    """
    print("=" * 60)
    print("ifm ZZ1350 IO-Link Master - Network Discovery")
    print("=" * 60)

    print("🔍 Step 1: Scanning ARP table...")
    arp_output = run_arp_command()

    if not arp_output:
        print("❌ Unable to get ARP table")
        return None

    print("✅ ARP table retrieved successfully")

    print("\n🔍 Step 2: Parsing device information...")
    devices = parse_arp_output(arp_output)

    if not devices:
        print("❌ No devices found in ARP table")
        return None

    print(f"✅ Found {len(devices)} devices in ARP table")

    print("\n🔍 Step 3: Looking for ifm devices...")

    # First, check for devices with ifm MAC addresses
    ifm_candidates = []
    for device in devices:
        if is_ifm_device(device["mac"]):
            ifm_candidates.append(device)
            print(f"🎯 Potential ifm device found:")
            print(f"   IP: {device['ip']}")
            print(f"   MAC: {device['mac']}")

    if not ifm_candidates:
        print("⚠️ No devices with known ifm MAC addresses found")
        print("🔍 Checking link-local addresses (169.254.x.x)...")

        # Look for link-local addresses as fallback
        for device in devices:
            if device["ip"].startswith("169.254."):
                ifm_candidates.append(device)

    if not ifm_candidates:
        print("❌ No potential IO-Link Master candidates found")
        print("\n💡 Troubleshooting tips:")
        print("   • Ensure IO-Link Master is powered on")
        print("   • Check Ethernet cable connections")
        print("   • Verify your computer is on the same network")
        return None

    print(f"\n🔍 Step 4: Testing {len(ifm_candidates)} candidate(s)...")

    for device in ifm_candidates:
        print(f"\n🧪 Testing {device['ip']} ({device['mac']})...")

        if test_iolink_connection(device["ip"]):
            print(f"✅ IO-Link Master found at {device['ip']}!")
            return device["ip"]
        else:
            print(f"❌ Not an IO-Link Master")

    print("\n❌ No IO-Link Master found")
    print("\n💡 Manual check suggestions:")
    print("   • Try accessing these IPs in your web browser:")
    for device in ifm_candidates:
        print(f"     http://{device['ip']}")

    return None


def main():
    """Main function"""
    try:
        discovered_ip = discover_iolink_master()

        if discovered_ip:
            print(f"\n" + "=" * 60)
            print("🎉 SUCCESS!")
            print("=" * 60)
            print(f"IO-Link Master discovered at: {discovered_ip}")
            print(f"Web interface: http://{discovered_ip}")
            print(f"\n💡 Update your Python scripts to use this IP address:")
            print(f'   master = IOLinkMaster("{discovered_ip}")')

            # Test basic functionality
            try:
                from iolink_master import IOLinkMaster

                print(f"\n🧪 Testing basic functionality...")
                master = IOLinkMaster(discovered_ip)
                port_count = master.get_port_count()
                print(f"✅ Device has {port_count} ports")
            except Exception as e:
                print(f"⚠️ Basic test failed: {e}")
        else:
            print(f"\n" + "=" * 60)
            print("❌ DISCOVERY FAILED")
            print("=" * 60)
            print("No IO-Link Master found on the network.")
            print("\n💡 Next steps:")
            print("   1. Check device power and network cables")
            print("   2. Verify network settings")
            print("   3. Try manual IP configuration")

    except KeyboardInterrupt:
        print("\n🛑 Discovery cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
