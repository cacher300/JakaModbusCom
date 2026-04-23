# JakaModbusCommunication

`JakaModbusCommunication` is a lightweight Python library for communicating with JAKA collaborative robots over Modbus TCP. It wraps common register reads and writes behind a small, task-focused API for digital I/O, analog values, and robot status data.

[PyPI package](https://pypi.org/project/JakaModbusCommunication/)

[Project page](https://lucaspijl.com/jaka-modbus-communication)

## Highlights

- Connect to a JAKA controller over Modbus TCP
- Read general, cabinet, and tool digital inputs
- Write digital outputs and analog outputs
- Read integer and floating-point register values
- Query robot telemetry such as joint voltage, temperature, current, position, speed, and TCP data
- Read controller status flags including power, enable, emergency stop, in-position state, and error indicators

## Installation

Install from PyPI:

```bash
pip install JakaModbusCommunication
```

The package depends on `pymodbus`, which is installed automatically.

## Quick Start

```python
from JakaModbusCommunication import Jaka_Coms

jaka = Jaka_Coms(host="192.168.1.186", port=502)

try:
    powered_on = jaka.get_power_on_status()
    joint_1_voltage = jaka.get_joint_voltage(1)
    tcp_x = jaka.get_tcp_position("X")

    print(f"Powered on: {bool(powered_on)}")
    print(f"Joint 1 voltage: {joint_1_voltage:.2f} V")
    print(f"TCP X: {tcp_x:.3f}")
finally:
    jaka.close()
```

## Common Operations

### Read digital inputs

```python
input_state = jaka.read_modbus_input_state(input_number=1)
cab_input = jaka.read_jaka_cab_input_state_mini(input_number=3)
tool_input = jaka.read_jaka_tool_input_state(input_number=1)
```

### Write digital outputs

```python
jaka.write_digital_modbus_output(output_number=5, state=True)
jaka.write_digital_cab_mini_output(output_number=2, state=False)
```

### Read analog values

```python
unsigned_value = jaka.read_int16(ao_number=3)
signed_value = jaka.read_sign16(ao_number=7)
float_value = jaka.read_float32(address=150)
```

### Write analog values

```python
jaka.write_analog_output_int(ao_number=4, value=1234)
jaka.write_analog_output_sign(ao_number=6, value=-123)
jaka.write_analog_output_float32(ao_number=2, value=12.34)
```

### Read robot status

```python
joint_voltage = jaka.get_joint_voltage(joint=1)
joint_position = jaka.get_joint_position(joint=3)
joint_temperature = jaka.get_joint_temperature(joint=2)
movement_mode = jaka.get_movement_mode()
```

## API Notes

- Joint-based methods accept joint numbers `1` through `6`.
- Axis-based TCP methods accept `"X"`, `"Y"`, `"Z"`, `"RX"`, `"RY"`, and `"RZ"`.
- Analog-output helper methods accept analog output numbers `1` through `16`.
- Floating-point values are encoded as big-endian 32-bit floats.
- The class connects automatically by default. Pass `auto_connect=False` if you want to control connection timing manually.

## Error Handling

The library raises:

- `ValueError` for invalid joint numbers, axis names, and analog output numbers
- `pymodbus.exceptions.ModbusException` when a Modbus request fails

Example:

```python
from pymodbus.exceptions import ModbusException

try:
    speed = jaka.get_joint_speed(joint=1)
except ValueError as exc:
    print(f"Invalid input: {exc}")
except ModbusException as exc:
    print(f"Modbus request failed: {exc}")
```

## Development

Clone the repository and install the package in editable mode:

```bash
pip install -e .
```

Run the tests:

```bash
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
