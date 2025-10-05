"""
Quick Device Scanner for ifm ZZ1350 IO-Link Master

This script demonstrates how to quickly scan all ports on your IO-Link Master
and display information about connected devices.

Usage:
    python quick_scanner.py

Requirements:
    - requests library
    - ifm AL1350 IO-Link Master connected to network
"""

import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from iolink_master import IOLinkMaster


def quick_scan(ip_address="169.254.178.135"):
    """
    Perform a quick scan of all ports on the IO-Link Master
    
    Args:
        ip_address (str): IP address of the IO-Link Master
    """
    print("=" * 60)
    print("ifm ZZ1350 IO-Link Master - Quick Device Scanner")
    print("=" * 60)
    
    try:
        # Initialize connection
        master = IOLinkMaster(ip_address)
        
        # Get port information
        port_count = master.get_port_count()
        print(f"📊 Total ports available: {port_count}")
        
        if port_count == 0:
            print("❌ No ports detected or connection failed")
            return
        
        # Scan each port
        connected_devices = 0
        for port in range(1, port_count + 1):
            print(f"\n🔍 Scanning Port {port}...")
            
            status = master.get_device_status(port)
            
            if status == "2":  # Device connected
                connected_devices += 1
                name = master.get_device_name(port)
                data = master.get_device_data(port)
                temp = master.get_temperature_celsius(port)
                
                print(f"✅ Device: {name}")
                print(f"📊 Current data: {data}")
                
                if temp is not None:
                    print(f"🌡️ Temperature: {temp:.1f}°C")
                else:
                    print("📊 Raw sensor data available")
            else:
                print("❌ No device connected")
        
        print(f"\n" + "=" * 60)
        print(f"✅ Scan complete! Found {connected_devices} connected device(s)")
        
        if connected_devices == 0:
            print("\n💡 Troubleshooting tips:")
            print("   • Check that sensors are properly connected")
            print("   • Verify power supply to IO-Link Master")
            print("   • Check network connection and IP address")
        
    except Exception as e:
        print(f"❌ Error during scan: {e}")
        print("\n💡 Common issues:")
        print("   • Wrong IP address - check your network settings")
        print("   • Network connectivity - ping the device first")
        print("   • Device not powered on or accessible")


if __name__ == "__main__":
    # You can change this IP address if your device uses DHCP
    DEVICE_IP = "169.254.178.135"
    
    print("Starting quick device scan...")
    print(f"Target device: {DEVICE_IP}")
    print("(Update DEVICE_IP variable if using DHCP)\n")
    
    quick_scan(DEVICE_IP)