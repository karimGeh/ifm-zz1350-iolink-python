"""
ifm ZZ1350 IO-Link Master Python Library

This module provides a Python interface for communicating with the ifm AL1350 IO-Link Master
using its REST API. It supports device discovery, sensor data reading, and real-time monitoring.

Author: Your Name
License: MIT
Repository: https://github.com/yourusername/ifm-zz1350-iolink-python
"""

import requests
import json
import time
from typing import Optional, Dict, Any, List


class IOLinkMaster:
    """
    Python interface for ifm AL1350 IO-Link Master
    
    This class provides methods to communicate with the ifm AL1350 IO-Link Master
    device using its REST API. It supports device discovery, sensor reading,
    and configuration management.
    
    Attributes:
        device_ip (str): IP address of the IO-Link Master
        base_url (str): Base URL for API requests
        timeout (int): Request timeout in seconds
    """
    
    def __init__(self, device_ip: str = "169.254.178.135", timeout: int = 5):
        """
        Initialize connection to IO-Link Master
        
        Args:
            device_ip (str): IP address of the IO-Link Master device
            timeout (int): Request timeout in seconds
            
        Raises:
            ConnectionError: If unable to connect to the device
        """
        self.device_ip = device_ip
        self.base_url = f"http://{device_ip}"
        self.timeout = timeout
        
        print(f"🔗 Connecting to IO-Link Master at {device_ip}")
        
        # Test connection
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            print("✅ Connection established")
        except requests.RequestException as e:
            print(f"❌ Connection failed: {e}")
            raise ConnectionError(f"Unable to connect to IO-Link Master at {device_ip}")
    
    def make_request(self, endpoint: str) -> Optional[str]:
        """
        Make a GET request to the IO-Link Master API
        
        Args:
            endpoint (str): API endpoint path
            
        Returns:
            str: Response data if successful, None if failed
            
        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                try:
                    # Try to parse as JSON first
                    data = response.json()
                    if 'data' in data:
                        return data['data']['value']
                    return str(data)
                except (json.JSONDecodeError, ValueError):
                    # Return raw text if not JSON
                    return response.text.strip()
            else:
                print(f"❌ Request failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ Request error: {e}")
            raise
    
    def get_port_count(self) -> int:
        """
        Get the number of available ports on the IO-Link Master
        
        Returns:
            int: Number of ports available
        """
        try:
            result = self.make_request("/iolinkmaster/port/numberofports/getdata")
            return int(result) if result else 0
        except (ValueError, TypeError):
            return 0
    
    def get_device_status(self, port: int) -> str:
        """
        Get the connection status of a device on a specific port
        
        Args:
            port (int): Port number (1-based)
            
        Returns:
            str: Device status ('2' = connected, '1' = disconnected, etc.)
        """
        return self.make_request(f"/iolinkmaster/port[{port}]/iolinkdevice/status/getdata") or "0"
    
    def get_device_name(self, port: int) -> str:
        """
        Get the product name of a device connected to a specific port
        
        Args:
            port (int): Port number (1-based)
            
        Returns:
            str: Device product name
        """
        return self.make_request(f"/iolinkmaster/port[{port}]/iolinkdevice/productname/getdata") or "Unknown"
    
    def get_device_data(self, port: int) -> str:
        """
        Get raw process data from a device on a specific port
        
        Args:
            port (int): Port number (1-based)
            
        Returns:
            str: Raw device data (hexadecimal format)
        """
        return self.make_request(f"/iolinkmaster/port[{port}]/iolinkdevice/pdin/getdata") or "0x0000"
    
    def get_temperature_celsius(self, port: int) -> Optional[float]:
        """
        Convert raw temperature sensor data to Celsius
        
        This method specifically handles TV7105 temperature sensor data conversion.
        
        Args:
            port (int): Port number (1-based)
            
        Returns:
            float: Temperature in Celsius, None if conversion fails
        """
        try:
            raw_data = self.get_device_data(port)
            if raw_data and raw_data.startswith('0x'):
                # Convert hex to integer
                hex_value = int(raw_data, 16)
                # TV7105 specific conversion: temperature = hex_value / 10
                temperature = hex_value / 10.0
                return temperature
        except (ValueError, TypeError) as e:
            print(f"❌ Temperature conversion error: {e}")
        return None
    
    def scan_all_ports(self) -> Dict[int, Dict[str, Any]]:
        """
        Scan all ports and return information about connected devices
        
        Returns:
            dict: Dictionary with port numbers as keys and device info as values
        """
        port_count = self.get_port_count()
        results = {}
        
        print(f"📊 Scanning {port_count} ports...")
        
        for port in range(1, port_count + 1):
            print(f"\n🔍 Scanning Port {port}...")
            
            status = self.get_device_status(port)
            
            port_info = {
                'port': port,
                'status': status,
                'connected': status == "2"
            }
            
            if status == "2":  # Device connected
                port_info.update({
                    'device_name': self.get_device_name(port),
                    'raw_data': self.get_device_data(port),
                    'temperature_c': self.get_temperature_celsius(port)
                })
                print(f"✅ Device: {port_info['device_name']}")
                print(f"📊 Raw data: {port_info['raw_data']}")
                if port_info['temperature_c'] is not None:
                    print(f"🌡️ Temperature: {port_info['temperature_c']:.1f}°C")
            else:
                print("❌ No device connected")
            
            results[port] = port_info
        
        return results
    
    def monitor_temperature(self, port: int, interval: int = 5, duration: Optional[int] = None):
        """
        Monitor temperature from a sensor in real-time
        
        Args:
            port (int): Port number to monitor
            interval (int): Seconds between readings
            duration (int): Total monitoring duration in seconds (None for infinite)
        """
        print(f"🌡️ Starting temperature monitoring on Port {port}")
        print(f"📊 Reading interval: {interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        start_time = time.time()
        
        try:
            while True:
                current_time = time.time()
                
                # Check duration limit
                if duration and (current_time - start_time) >= duration:
                    print(f"\n⏰ Monitoring completed ({duration} seconds)")
                    break
                
                temperature = self.get_temperature_celsius(port)
                timestamp = time.strftime("%H:%M:%S")
                
                if temperature is not None:
                    print(f"[{timestamp}] 🌡️ Port {port}: {temperature:.1f}°C")
                else:
                    print(f"[{timestamp}] ❌ Port {port}: Unable to read temperature")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Monitoring stopped by user")


def hex_to_temperature(hex_value: str) -> Optional[float]:
    """
    Utility function to convert hex temperature data to Celsius
    
    Args:
        hex_value (str): Hexadecimal temperature value (e.g., '0x0157')
        
    Returns:
        float: Temperature in Celsius, None if conversion fails
    """
    try:
        if hex_value and hex_value.startswith('0x'):
            decimal_value = int(hex_value, 16)
            return decimal_value / 10.0
    except (ValueError, TypeError, AttributeError):
        pass
    return None


if __name__ == "__main__":
    # Example usage
    try:
        # Initialize connection
        master = IOLinkMaster("169.254.178.135")
        
        # Scan all ports
        devices = master.scan_all_ports()
        
        # Find connected temperature sensors
        for port, info in devices.items():
            if info['connected'] and info.get('temperature_c') is not None:
                print(f"\n🎯 Found temperature sensor on Port {port}")
                print(f"Starting 30-second monitoring session...")
                master.monitor_temperature(port, interval=2, duration=30)
                break
        else:
            print("\n❌ No temperature sensors found")
            
    except Exception as e:
        print(f"❌ Error: {e}")