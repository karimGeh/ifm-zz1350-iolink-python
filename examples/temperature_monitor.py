"""
Temperature Monitor for ifm ZZ1350 IO-Link Master

This script demonstrates continuous temperature monitoring from a TV7105 
temperature sensor connected to your IO-Link Master.

Usage:
    python temperature_monitor.py [port] [interval]

Arguments:
    port (int): Port number to monitor (default: 1)
    interval (int): Seconds between readings (default: 5)

Examples:
    python temperature_monitor.py              # Monitor port 1 every 5 seconds
    python temperature_monitor.py 2            # Monitor port 2 every 5 seconds  
    python temperature_monitor.py 1 2          # Monitor port 1 every 2 seconds

Requirements:
    - requests library
    - TV7105 temperature sensor connected to IO-Link Master
"""

import sys
import os
import time

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from iolink_master import IOLinkMaster


def monitor_temperature_advanced(ip_address="169.254.178.135", port=1, interval=5):
    """
    Advanced temperature monitoring with statistics and alerts
    
    Args:
        ip_address (str): IP address of the IO-Link Master
        port (int): Port number to monitor
        interval (int): Seconds between readings
    """
    print("=" * 60)
    print("ifm ZZ1350 IO-Link Master - Temperature Monitor")
    print("=" * 60)
    
    try:
        # Initialize connection
        master = IOLinkMaster(ip_address)
        
        # Verify device is connected on specified port
        status = master.get_device_status(port)
        if status != "2":
            print(f"❌ No device connected on Port {port}")
            print("💡 Use the quick_scanner.py to find connected devices")
            return
        
        device_name = master.get_device_name(port)
        print(f"📊 Monitoring device: {device_name} on Port {port}")
        print(f"⏰ Reading interval: {interval} seconds")
        print("📈 Press Ctrl+C to stop and see statistics\n")
        
        # Statistics tracking
        temperatures = []
        start_time = time.time()
        reading_count = 0
        
        try:
            while True:
                reading_count += 1
                temperature = master.get_temperature_celsius(port)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                if temperature is not None:
                    temperatures.append(temperature)
                    
                    # Calculate running statistics
                    if len(temperatures) > 1:
                        min_temp = min(temperatures)
                        max_temp = max(temperatures)
                        avg_temp = sum(temperatures) / len(temperatures)
                        
                        print(f"[{timestamp}] 🌡️ {temperature:.1f}°C | "
                              f"Min: {min_temp:.1f}°C | Max: {max_temp:.1f}°C | "
                              f"Avg: {avg_temp:.1f}°C")
                    else:
                        print(f"[{timestamp}] 🌡️ {temperature:.1f}°C")
                    
                    # Simple alert system
                    if temperature > 30.0:
                        print(f"🔥 HIGH TEMPERATURE ALERT: {temperature:.1f}°C")
                    elif temperature < 10.0:
                        print(f"🧊 LOW TEMPERATURE ALERT: {temperature:.1f}°C")
                        
                else:
                    print(f"[{timestamp}] ❌ Failed to read temperature")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            # Display final statistics
            total_time = time.time() - start_time
            print(f"\n" + "=" * 60)
            print("📊 MONITORING STATISTICS")
            print("=" * 60)
            print(f"📈 Total readings: {reading_count}")
            print(f"⏰ Total time: {total_time:.1f} seconds")
            print(f"📊 Average interval: {total_time/reading_count:.1f} seconds")
            
            if temperatures:
                print(f"🌡️ Temperature Statistics:")
                print(f"   • Minimum: {min(temperatures):.1f}°C")
                print(f"   • Maximum: {max(temperatures):.1f}°C")
                print(f"   • Average: {sum(temperatures)/len(temperatures):.1f}°C")
                print(f"   • Range: {max(temperatures) - min(temperatures):.1f}°C")
                print(f"   • Valid readings: {len(temperatures)}/{reading_count}")
            
            print("\n🛑 Monitoring stopped by user")
    
    except Exception as e:
        print(f"❌ Error during monitoring: {e}")


def main():
    """Main function to handle command line arguments"""
    # Default values
    DEVICE_IP = "169.254.178.135"
    port = 1
    interval = 5
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default: 1")
    
    if len(sys.argv) > 2:
        try:
            interval = int(sys.argv[2])
            if interval < 1:
                print("❌ Interval must be at least 1 second. Using default: 5")
                interval = 5
        except ValueError:
            print("❌ Invalid interval. Using default: 5 seconds")
    
    print(f"Configuration:")
    print(f"• Device IP: {DEVICE_IP}")
    print(f"• Port: {port}")
    print(f"• Interval: {interval} seconds")
    print("(Update DEVICE_IP in script if using DHCP)\n")
    
    monitor_temperature_advanced(DEVICE_IP, port, interval)


if __name__ == "__main__":
    main()