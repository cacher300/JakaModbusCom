# JAKA_Coms Library README

## Overview

`JAKA_Coms` is a Python library for communicating with JAKA collaborative robots (cobots) over Modbus TCP. This library provides functionality for reading and writing discrete inputs, outputs, and analog values, as well as retrieving various system and sensor data.

---

## Features

- **Digital Input/Output Handling**:
  - Read and write the states of digital inputs and outputs.
  - Support for specific JAKA input/output types such as `CAB`, `TOOL`, and `MINI`.

- **Analog Input/Output Handling**:
  - Read and write 16-bit integer, signed integer, and 32-bit floating-point values to analog outputs.

- **System Data**:
  - Retrieve data such as servo version, serial numbers, joint data (voltages, temperatures, positions, etc.), TCP position and speed, control status, and cabinet data.

- **Modbus TCP Connection Management**:
  - Easy connection and disconnection from a Modbus TCP server.
  - Automatic connection option.

---

## Installation

To use `JAKA_Coms`, you need to have the following Python package installed:

- `pymodbus`

Install it via pip if not already available:

```bash
pip install pymodbus
```

---

## Getting Started

### Initialization

Create an instance of the `Jaka_Coms` class with the Modbus server's IP address and port:

```python
from JakaModbusCommunication import Jaka_Coms

# Initialize the connection
jaka = Jaka_Coms(host="192.168.1.10", port=502, auto_connect=True)
```

### Example Usage

#### Reading Digital Input State
```python
input_number = 1
state = jaka.read_modbus_input_state(input_number)
print(f"Input {input_number} state: {state}")
```

#### Writing Digital Output State
```python
output_number = 1
jaka.write_digital_modbus_output(output_number, state=True)
print(f"Output {output_number} set to ON")
```

#### Reading Analog Output as Float
```python
ao_number = 1
value = jaka.read_float32(ao_number)
print(f"AO{ao_number} value: {value}")
```

#### Writing Analog Output as Float
```python
ao_number = 1
jaka.write_analog_output_float32(ao_number, value=12.34)
print(f"Set AO{ao_number} to 12.34")
```

#### Reading Joint Data
```python
joint = 1
position = jaka.get_joint_position(joint)
print(f"Joint {joint} position: {position}")
```

### Closing the Connection
```python
jaka.close()
```

---

## Class Methods

### Connection Management
- `connect()`: Establish a connection.
- `close()`: Close the connection.
- `__del__()`: Destructor to ensure the connection is closed.

### Digital Input/Output
- `read_modbus_input_state(input_number)`: Read the state of a digital input.
- `write_digital_modbus_output(output_number, state)`: Write the state of a digital output.

### Analog Input/Output
- `read_int16(ao_number)`: Read a 16-bit unsigned integer analog output.
- `read_sign16(ao_number)`: Read a 16-bit signed integer analog output.
- `read_float32(ao_number)`: Read a 32-bit floating-point analog output.
- `write_analog_output_int(ao_number, value)`: Write a 16-bit unsigned integer analog output.
- `write_analog_output_float32(ao_number, value)`: Write a 32-bit floating-point analog output.

### System Data
- Retrieve servo versions, joint data, TCP position, and cabinet data using various methods like:
  - `get_joint_position(joint)`
  - `get_tcp_position(axis)`
  - `get_cab_temperature()`

---

## Error Handling

Errors during Modbus operations are raised as exceptions (`ModbusException`). Ensure to handle these in your implementation to avoid runtime crashes.

Example:
```python
try:
    state = jaka.read_modbus_input_state(1)
except ModbusException as e:
    print(f"Error reading input: {e}")
```

---

## License

This library is licensed under [Your License Here]. Replace this with the actual license details.

---

## Contribution

Contributions to enhance this library are welcome. Submit a pull request or open an issue on the repository.

---

## Disclaimer

This library assumes familiarity with JAKA cobots and the Modbus protocol. Refer to JAKA's official documentation for more details on register mappings and functionalities.
