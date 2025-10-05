# API Reference

## IOLinkMaster Class

The main class for communicating with the ifm AL1350 IO-Link Master.

### Constructor

```python
IOLinkMaster(device_ip="169.254.178.135", timeout=5)
```

**Parameters:**
- `device_ip` (str): IP address of the IO-Link Master device
- `timeout` (int): Request timeout in seconds

**Raises:**
- `ConnectionError`: If unable to connect to the device

### Core Methods

#### `make_request(endpoint)`

Make a GET request to the IO-Link Master API.

**Parameters:**
- `endpoint` (str): API endpoint path

**Returns:**
- `str`: Response data if successful, None if failed

**Raises:**
- `requests.RequestException`: If request fails

#### `get_port_count()`

Get the number of available ports on the IO-Link Master.

**Returns:**
- `int`: Number of ports available

#### `get_device_status(port)`

Get the connection status of a device on a specific port.

**Parameters:**
- `port` (int): Port number (1-based)

**Returns:**
- `str`: Device status ('2' = connected, '1' = disconnected, etc.)

#### `get_device_name(port)`

Get the product name of a device connected to a specific port.

**Parameters:**
- `port` (int): Port number (1-based)

**Returns:**
- `str`: Device product name

#### `get_device_data(port)`

Get raw process data from a device on a specific port.

**Parameters:**
- `port` (int): Port number (1-based)

**Returns:**
- `str`: Raw device data (hexadecimal format)

#### `get_temperature_celsius(port)`

Convert raw temperature sensor data to Celsius (TV7105 specific).

**Parameters:**
- `port` (int): Port number (1-based)

**Returns:**
- `float`: Temperature in Celsius, None if conversion fails

#### `scan_all_ports()`

Scan all ports and return information about connected devices.

**Returns:**
- `dict`: Dictionary with port numbers as keys and device info as values

#### `monitor_temperature(port, interval=5, duration=None)`

Monitor temperature from a sensor in real-time.

**Parameters:**
- `port` (int): Port number to monitor
- `interval` (int): Seconds between readings
- `duration` (int): Total monitoring duration in seconds (None for infinite)

## Utility Functions

#### `hex_to_temperature(hex_value)`

Convert hex temperature data to Celsius.

**Parameters:**
- `hex_value` (str): Hexadecimal temperature value (e.g., '0x0157')

**Returns:**
- `float`: Temperature in Celsius, None if conversion fails

## Device Status Codes

- `"0"` - No device/error
- `"1"` - Device detected but not operational
- `"2"` - Device connected and operational
- `"3"` - Device in configuration mode

## Temperature Conversion

For TV7105 temperature sensor:
- Raw data format: Hexadecimal (e.g., "0x0157")
- Conversion: `temperature_celsius = hex_to_decimal / 10.0`
- Example: 0x0157 = 343 decimal = 34.3°C