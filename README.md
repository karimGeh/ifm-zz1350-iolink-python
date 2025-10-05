# ifm ZZ1350 IO-Link Master Python Library

A Python library and example scripts for communicating with the **ifm AL1350 IO-Link Master** using its REST API. This repository contains all the code examples from the LinkedIn article **"ifm ZZ1350 IO-Link Master Kit: Getting Started with Industrial IoT"**.

## 📖 Background

This repository accompanies the comprehensive LinkedIn tutorial that guides you through:
- Setting up the ifm ZZ1350 starter kit
- Network discovery and configuration  
- Building Python applications for industrial sensor monitoring
- Real-world industrial IoT implementation

**📚 Read the full article**: [ifm ZZ1350 IO-Link Master Kit: Getting Started with Industrial IoT](YOUR_LINKEDIN_ARTICLE_URL)

## 🎯 What This Repository Contains

### Core Library (`src/`)
- **`iolink_master.py`** - Main Python class for IO-Link Master communication
- Complete API wrapper with error handling and documentation
- Temperature sensor data conversion utilities
- Real-time monitoring capabilities

### Example Scripts (`examples/`)
- **`quick_scanner.py`** - Scan all ports and discover connected devices
- **`temperature_monitor.py`** - Continuous temperature monitoring with statistics

### Utility Scripts (`scripts/`)
- **`network_discovery.py`** - Network discovery using ARP protocol (from article)

### Tests (`tests/`)
- **`test_iolink_master.py`** - Comprehensive unit tests
- **`conftest.py`** - pytest configuration
- Mock tests for development without hardware
- Integration tests for real device validation

## 🚀 Quick Start

### Prerequisites

1. **Hardware**: ifm ZZ1350 IO-Link Master starter kit with TV7105 temperature sensor
2. **Python**: 3.7 or higher
3. **Network**: IO-Link Master connected to your network

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/ifm-zz1350-iolink-python.git
   cd ifm-zz1350-iolink-python
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Find your device** (if you don't know the IP):
   ```bash
   python scripts/network_discovery.py
   ```

### Basic Usage

**Quick device scan**:
```bash
python examples/quick_scanner.py
```

**Monitor temperature in real-time**:
```bash
python examples/temperature_monitor.py
```

**Use in your own code**:
```python
from src.iolink_master import IOLinkMaster

# Connect to your IO-Link Master
master = IOLinkMaster("169.254.178.135")  # Use your device's IP

# Scan all ports
devices = master.scan_all_ports()

# Monitor temperature on port 1
master.monitor_temperature(port=1, interval=5)
```

## 📁 Repository Structure

```
ifm-zz1350-iolink-python/
├── src/
│   └── iolink_master.py          # Main library
├── examples/
│   ├── quick_scanner.py          # Device discovery example
│   └── temperature_monitor.py    # Temperature monitoring example
├── scripts/
│   └── network_discovery.py     # Network discovery utility
├── tests/
│   ├── test_iolink_master.py     # Unit tests
│   └── conftest.py               # Test configuration
├── docs/
│   └── API.md                    # API documentation
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Configuration

### IP Address Configuration

The default IP address in all scripts is `169.254.178.135` (link-local address). 

**If you completed the DHCP configuration steps from the article**:
1. Find your device's new IP address from your router's DHCP client list
2. Update the `DEVICE_IP` variable in each script, or
3. Pass the IP address as a parameter to the `IOLinkMaster` class

### Network Discovery

If you're unsure of your device's IP address, use the network discovery script:

```bash
python scripts/network_discovery.py
```

This script implements the ARP-based discovery method explained in the LinkedIn article.

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python -m pytest tests/ -v

# Run only unit tests (no hardware required)
python -m pytest tests/ -v -m "not integration"

# Run integration tests (requires real hardware)
python -m pytest tests/ -v -m integration
```

## 📊 Examples Output

### Quick Scanner
```
===============================================================
ifm ZZ1350 IO-Link Master - Quick Device Scanner
===============================================================
🔗 Connecting to IO-Link Master at 169.254.178.135
✅ Connection established
📊 Total ports available: 4

🔍 Scanning Port 1...
✅ Device: TV7105
📊 Current data: 0x0157
🌡️ Temperature: 34.3°C

🔍 Scanning Port 2...
❌ No device connected
```

### Temperature Monitor
```
===============================================================
ifm ZZ1350 IO-Link Master - Temperature Monitor
===============================================================
📊 Monitoring device: TV7105 on Port 1
⏰ Reading interval: 5 seconds
📈 Press Ctrl+C to stop and see statistics

[2024-10-05 14:30:15] 🌡️ 24.3°C
[2024-10-05 14:30:20] 🌡️ 24.4°C | Min: 24.3°C | Max: 24.4°C | Avg: 24.4°C
```

## 🔌 Supported Devices

### IO-Link Masters
- **ifm AL1350** (ZZ1350 starter kit) ✅

### Sensors  
- **ifm TV7105** temperature sensor ✅
- Other IO-Link sensors (basic data reading) ✅

## 🛠️ API Reference

### IOLinkMaster Class

**Constructor**:
```python
IOLinkMaster(device_ip="169.254.178.135", timeout=5)
```

**Key Methods**:
- `get_port_count()` - Get number of available ports
- `get_device_status(port)` - Check if device is connected on port
- `get_device_name(port)` - Get product name of connected device
- `get_device_data(port)` - Get raw sensor data
- `get_temperature_celsius(port)` - Convert temperature sensor data to Celsius
- `scan_all_ports()` - Scan all ports and return device information
- `monitor_temperature(port, interval, duration)` - Real-time temperature monitoring

**Utility Functions**:
- `hex_to_temperature(hex_value)` - Convert hex temperature data to Celsius

For detailed API documentation, see [`docs/API.md`](docs/API.md).

## 🔍 Troubleshooting

### Common Issues

**Connection refused or timeout**:
- Check IP address and network connectivity
- Verify device is powered on
- Try network discovery script: `python scripts/network_discovery.py`

**No devices found on ports**:
- Check sensor connections and power
- Verify sensors are IO-Link compatible
- Check device status via web interface: `http://YOUR_DEVICE_IP`

**Import errors**:
- Ensure you're running scripts from the repository root
- Install requirements: `pip install -r requirements.txt`

### Getting Help

1. **Check the LinkedIn article** for setup and configuration details
2. **Run the network discovery script** to verify device connectivity
3. **Check device web interface** at `http://YOUR_DEVICE_IP`
4. **Run unit tests** to verify library functionality

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. **Report bugs** - Open an issue with details
2. **Suggest features** - Share your ideas for improvements  
3. **Submit pull requests** - Follow standard GitHub workflow
4. **Share your projects** - Let us know what you've built!

### Development Setup

1. Clone the repository
2. Install development dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest tests/ -v`
4. Follow PEP 8 style guidelines

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ifm electronic** for the excellent ZZ1350 starter kit and documentation
- **IO-Link community** for the comprehensive protocol specifications
- **LinkedIn readers** who provided feedback and suggestions on the original article

## 📞 Support

- **LinkedIn**: Connect with me for questions about the article
- **GitHub Issues**: Report bugs or request features
- **ifm Support**: For hardware-specific questions, contact ifm electronic

---

**⭐ Found this helpful?** Give this repository a star and share the LinkedIn article!

**🔗 Related Resources**:
- [ifm electronic IO-Link Academy](https://www.ifm.com/academy)
- [IO-Link Official Specification](https://io-link.com/)
- [Original LinkedIn Article](YOUR_LINKEDIN_ARTICLE_URL)