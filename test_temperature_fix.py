#!/usr/bin/env python3
"""
Quick test to verify the corrected temperature conversion
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from iolink_master import IOLinkMaster, hex_to_temperature


def test_current_temperature():
    """Test with the actual sensor data we're getting"""

    # Current sensor readings from the device
    current_raw_data = "013BFF00"  # What we're currently reading

    print("🧪 Testing Temperature Conversion")
    print("=" * 50)

    # Extract first 4 hex digits
    temp_hex = current_raw_data[:4]
    hex_value = int(temp_hex, 16)

    print(f"📊 Raw data: {current_raw_data}")
    print(f"🔢 Temperature hex: 0x{temp_hex}")
    print(f"🔢 Decimal value: {hex_value}")

    # Old wrong formula
    old_temp = hex_value / 10.0
    print(f"❌ Old formula (wrong): {hex_value} / 10 = {old_temp:.1f}°C")

    # Correct formula from LinkedIn tutorial
    correct_temp = (hex_value - 100) / 10.0
    print(f"✅ Correct formula: ({hex_value} - 100) / 10 = {correct_temp:.1f}°C")

    # Test with utility function
    util_result = hex_to_temperature(f"0x{temp_hex}")
    print(f"🔧 Utility function result: {util_result:.1f}°C")

    print("\n🌡️ Temperature Analysis:")
    print(f"   Room temperature should be ~24°C (according to weather)")
    print(f"   Old reading: {old_temp:.1f}°C (too high! ❌)")
    print(f"   New reading: {correct_temp:.1f}°C (realistic! ✅)")

    return correct_temp


if __name__ == "__main__":
    test_current_temperature()

    print("\n🚀 Testing with real device...")
    try:
        master = IOLinkMaster("192.168.1.101")
        temp = master.get_temperature_celsius(1)
        print(f"🌡️ Live temperature reading: {temp:.1f}°C")
    except Exception as e:
        print(f"❌ Could not connect to device: {e}")
