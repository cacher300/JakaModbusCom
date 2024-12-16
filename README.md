
# JakaModbusCommunication Library

`JakaModbusCommunication` is a Python library that simplifies Modbus TCP communication for reading and writing discrete inputs, coils, and analog outputs (e.g., `UINT16`, `INT16`, and `FLOAT32`). It is built on top of the **`pymodbus`** library and provides easy-to-use methods for interacting with Modbus-enabled devices.

---

## Features

- **Read Discrete Inputs**: General inputs, CAB inputs, Tool inputs.
- **Write Coils (Outputs)**: Digital outputs, CAB outputs, Tool outputs.
- **Read Analog Outputs**: Supports `UINT16`, `INT16`, and `FLOAT32` values.
- **Write Analog Outputs**: Allows writing of `FLOAT32` and `UINT16` values.
- **Read Robot Data**: Retrieve joint voltages, temperatures, currents, and TCP position/speed.

---

## Installation

To use the Modbus Helper library, install the required dependencies:

```bash
pip install pymodbus
```

---

## Usage

### 1. Initialize JakaModbusCommunication

Import and create an instance of `JakaModbusCommunication`:

```python
from JakaModbusCommunication import Jaka_Coms

# Initialize the Modbus client
jaka_coms = Jaka_Coms(host="192.168.1.101", port=502)  # Replace with your Modbus server IP

try:
    # Set AO (Analog Output) channel 1 to value 6
    ao_channel = 2  # Modify this for the specific AO channel you want
    value_to_set = 6
    jaka_coms.write_analog_output_int(ao_number=ao_channel, value=value_to_set)

    print(f"Successfully set AO{ao_channel} to {value_to_set}.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the connection
    jaka_coms.close()

```

---

## Methods

### **Connection Management**
| Method                        | Description                                      |
|-------------------------------|--------------------------------------------------|
| `connect()`                   | Connects to the Modbus TCP server.              |
| `close()`                     | Closes the connection to the Modbus server.     |

---

### **Read Digital Inputs**
| Method                             | Description                                   |
|------------------------------------|-----------------------------------------------|
| `read_digital_input(input_number)` | Reads a general digital input state.          |
| `read_cab_input_mini(input_number)`| Reads CAB mini input state (1–7).             |
| `read_cab_input_zu(input_number)`  | Reads CAB input state for Jaka Zu inputs.     |
| `read_tool_input(input_number)`    | Reads Tool input state (1–2).                 |

---

### **Write Digital Outputs**
| Method                                 | Description                                  |
|----------------------------------------|----------------------------------------------|
| `write_digital_output(output_number, state)` | Writes a state (ON/OFF) to a digital output. |
| `write_cab_output_mini(output_number, state)`| Writes to CAB Mini digital outputs (1–7).    |

---

### **Read Analog Outputs**
| Method                                   | Description                                  |
|------------------------------------------|----------------------------------------------|
| `read_analog_output_uint16(ao_number)`   | Reads a `UINT16` analog output value.        |
| `read_analog_output_int16(ao_number)`    | Reads an `INT16` analog output value.        |
| `read_analog_output_float32(ao_number)`  | Reads a `FLOAT32` analog output value.       |

---

### **Write Analog Outputs**
| Method                                   | Description                                  |
|------------------------------------------|----------------------------------------------|
| `write_analog_output_int(ao_number, value)`    | Writes a `UINT16` analog output value.       |
| `write_analog_output_float32(ao_number, value)`| Writes a `FLOAT32` analog output value.      |

---

### **Robot Data Methods**
| Method                                  | Description                                   |
|-----------------------------------------|-----------------------------------------------|
| `get_servo_version()`                   | Reads the servo version number.               |
| `get_robot_serial_no()`                 | Reads the robot serial number.                |
| `get_joint_voltage(joint)`              | Reads the voltage of a specific joint.        |
| `get_joint_temperature(joint)`          | Reads the temperature of a specific joint.    |
| `get_joint_servo_error_code(joint)`     | Reads the servo error code for a joint.       |
| `get_joint_position(joint)`             | Reads the position of a joint.                |
| `get_tcp_position(axis)`                | Reads TCP position (`X`, `Y`, `Z`, `RX`, etc.).|
| `get_tcp_speed(axis)`                   | Reads TCP speed (`X`, `Y`, `Z`, `RX`, etc.).  |
| `get_collision_protective_stop()`       | Checks for collision protection stop.         |
| `get_emergency_stop()`                  | Reads the emergency stop state.               |

---

## Modbus Address Mapping

### Digital Inputs
| Type                | Address Range  | Notes                                  |
|---------------------|----------------|----------------------------------------|
| General Inputs      | 8–135          | Includes DO1 to DO128.                 |
| CAB Mini Inputs     | 136–143        | CAB DI1 to CAB DI8.                    |
| Tool Inputs         | 152–153        | TOOL DI1, TOOL DI2.                    |

### Digital Outputs
| Type                | Address Range  | Notes                                  |
|---------------------|----------------|----------------------------------------|
| General Outputs     | 40–167         | DI1 to DI128.                          |
| CAB Outputs         | 168–183        | CAB DO1 to CAB DO16.                   |
| Tool Outputs        | 184–185        | TOOL DO1, TOOL DO2.                    |

### Analog Outputs
| Type                | Address Range  | Data Type                              |
|---------------------|----------------|----------------------------------------|
| Analog UINT16       | 96–115         | UINT16                                 |
| Analog INT16        | 112–120        | INT16                                  |
| Analog FLOAT32      | 128–164        | FLOAT32 (big-endian display).          |

---

## Requirements

- Python 3.6+
- `pymodbus` library

Install the required library using:

```bash
pip install pymodbus
```

---

## Example: Robot Data Retrieval

```python
from JakaModbusCommunication import Jaka_Coms

# Initialize the Modbus client
jaka_coms = Jaka_Coms(host="192.168.1.101", port=502)  # Replace with your Modbus server IP

try:
    # Set AO (Analog Output) channel 1 to value 6
    ao_channel = 2  # Modify this for the specific AO channel you want
    value_to_set = 6
    jaka_coms.write_analog_output_int(ao_number=ao_channel, value=value_to_set)

    print(f"Successfully set AO{ao_channel} to {value_to_set}.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the connection
    jaka_coms.close()

```
---

## Contributing

Feel free to open pull requests or issues to improve this library.

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

Let me know if you'd like further refinements! 🚀
