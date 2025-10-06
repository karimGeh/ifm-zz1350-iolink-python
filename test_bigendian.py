#!/usr/bin/env python3
"""
Test BigEndian format interpretation for TV7105 temperature data
"""

import struct


def test_bigendian_interpretation():
    """Test if we need to handle BigEndian format differently"""

    # Current sensor reading
    current_raw_data = "0139FF00"

    print("🧪 Testing BigEndian vs LittleEndian Interpretation")
    print("=" * 55)

    print(f"📊 Raw data: {current_raw_data}")

    # Convert to bytes
    raw_bytes = bytes.fromhex(current_raw_data)
    print(f"🔢 Raw bytes: {[hex(b) for b in raw_bytes]}")

    # Method 1: Simple hex to int (what we're doing now)
    temp_hex = current_raw_data[:4]  # First 16 bits
    simple_value = int(temp_hex, 16)
    simple_temp = simple_value * 0.1
    print(f"\n📝 Method 1 (Current): First 4 hex chars")
    print(f"   Hex: 0x{temp_hex} = {simple_value} decimal")
    print(f"   Temperature: {simple_value} * 0.1 = {simple_temp:.1f}°C")

    # Method 2: BigEndian 16-bit interpretation
    # First 2 bytes as BigEndian 16-bit integer
    bigendian_value = struct.unpack(">H", raw_bytes[:2])[
        0
    ]  # >H = BigEndian unsigned short
    bigendian_temp = bigendian_value * 0.1
    print(f"\n📝 Method 2: BigEndian 16-bit from first 2 bytes")
    print(f"   Bytes: {raw_bytes[:2].hex()} = {bigendian_value} decimal")
    print(f"   Temperature: {bigendian_value} * 0.1 = {bigendian_temp:.1f}°C")

    # Method 3: LittleEndian 16-bit interpretation
    littleendian_value = struct.unpack("<H", raw_bytes[:2])[
        0
    ]  # <H = LittleEndian unsigned short
    littleendian_temp = littleendian_value * 0.1
    print(f"\n📝 Method 3: LittleEndian 16-bit from first 2 bytes")
    print(f"   Bytes: {raw_bytes[:2].hex()} = {littleendian_value} decimal")
    print(f"   Temperature: {littleendian_value} * 0.1 = {littleendian_temp:.1f}°C")

    # Method 4: Maybe temperature is in a different position?
    # Last 2 bytes
    last_bytes_value = struct.unpack(">H", raw_bytes[2:])[0]
    last_bytes_temp = last_bytes_value * 0.1
    print(f"\n📝 Method 4: BigEndian 16-bit from last 2 bytes")
    print(f"   Bytes: {raw_bytes[2:].hex()} = {last_bytes_value} decimal")
    print(f"   Temperature: {last_bytes_value} * 0.1 = {last_bytes_temp:.1f}°C")

    print(f"\n🌡️ Results Summary:")
    print(f"   Method 1 (current): {simple_temp:.1f}°C")
    print(f"   Method 2 (BigEndian): {bigendian_temp:.1f}°C")
    print(f"   Method 3 (LittleEndian): {littleendian_temp:.1f}°C")
    print(f"   Method 4 (Last 2 bytes): {last_bytes_temp:.1f}°C")

    # Check which method gives reasonable room temperature
    methods = [
        ("Method 1", simple_temp),
        ("Method 2", bigendian_temp),
        ("Method 3", littleendian_temp),
        ("Method 4", last_bytes_temp),
    ]

    print(f"\n✅ Reasonable room temperature (20-30°C):")
    for name, temp in methods:
        if 20 <= temp <= 30:
            print(f"   {name}: {temp:.1f}°C ✅")
        else:
            print(f"   {name}: {temp:.1f}°C ❌")


if __name__ == "__main__":
    test_bigendian_interpretation()
