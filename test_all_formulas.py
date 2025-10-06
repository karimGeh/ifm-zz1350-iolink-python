#!/usr/bin/env python3
"""
Test all three temperature conversion formulas with actual sensor data
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_all_formulas():
    """Test all three formulas we've tried"""

    # Current sensor readings from the device
    current_raw_data = "013BFF00"  # What we're currently reading

    print("🧪 Testing All Temperature Conversion Formulas")
    print("=" * 60)

    # Extract first 4 hex digits (16-bit temperature data)
    temp_hex = current_raw_data[:4]
    hex_value = int(temp_hex, 16)

    print(f"📊 Raw data: {current_raw_data}")
    print(f"🔢 Temperature hex: 0x{temp_hex}")
    print(f"🔢 Decimal value: {hex_value}")
    print()

    # Formula 1: Original wrong formula
    formula1 = hex_value / 10.0
    print(f"❌ Formula 1 (original): {hex_value} / 10 = {formula1:.1f}°C")

    # Formula 2: LinkedIn tutorial formula
    formula2 = (hex_value - 100) / 10.0
    print(f"📝 Formula 2 (LinkedIn): ({hex_value} - 100) / 10 = {formula2:.1f}°C")

    # Formula 3: Official PDF formula
    formula3 = hex_value * 0.1
    print(f"📋 Formula 3 (Official PDF): {hex_value} * 0.1 = {formula3:.1f}°C")

    print("\n🌡️ Analysis:")
    print(f"   Expected room temp: ~24°C (weather reference)")
    print(
        f"   Formula 1: {formula1:.1f}°C - {'✅ Close to room temp' if 20 <= formula1 <= 30 else '❌ Too hot/cold'}"
    )
    print(
        f"   Formula 2: {formula2:.1f}°C - {'✅ Close to room temp' if 20 <= formula2 <= 30 else '❌ Too hot/cold'}"
    )
    print(
        f"   Formula 3: {formula3:.1f}°C - {'✅ Close to room temp' if 20 <= formula3 <= 30 else '❌ Too hot/cold'}"
    )

    print("\n🤔 Note: Formula 1 and 3 give the same result!")
    print("This suggests the official PDF formula might be correct,")
    print("but the LinkedIn tutorial formula gave more reasonable room temp.")

    # Let's also check if the sensor might be reading something else
    print("\n🔍 Additional Analysis:")
    print("Maybe the sensor is reading:")
    print(f"   - Actual air temperature: {formula3:.1f}°C")
    print(f"   - Or sensor internal temperature (could be slightly warm)")
    print(f"   - Or there's a different data interpretation needed")


if __name__ == "__main__":
    test_all_formulas()
