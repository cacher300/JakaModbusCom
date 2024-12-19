# JakaModbusCommunication Library

This library provides an interface to communicate with Jaka collaborative robots over Modbus TCP, enabling reading and writing of registers, controlling I/O, and retrieving robot status data.

---

## Features
- Connect to Modbus TCP servers.
- Read and write digital inputs/outputs.
- Read and write analog values (integer and floating-point).
- Access robot-specific data such as joint position, voltage, and speed.
- Monitor the robot's power, motion status, and error codes.

---

## Installation

Install the required dependency:

```bash
pip install pymodbus
```

---

## Getting Started

### Import and Initialize

```python
from JakaModbusCommunication import Jaka_Coms

# Initialize the Modbus communication with the robot
jaka = Jaka_Coms(host="192.168.1.186", port=502)  # Replace with your robot's IP
```

---

## Examples

### Reading Digital Inputs

```python
# Read the state of discrete input 1
input_state = jaka.read_modbus_input_state(input_number=1)
print(f"Input 1 State: {input_state}")
```

---

### Writing Digital Outputs

```python
# Set digital output 5 to ON
jaka.write_digital_modbus_output(output_number=5, state=True)

# Set digital output 5 to OFF
jaka.write_digital_modbus_output(output_number=5, state=False)
```

---

### Reading Analog Values

```python
# Read unsigned 16-bit value from analog output 3
analog_value = jaka.read_int16(ao_number=3)
print(f"Analog Output 3 Value: {analog_value}")

# Read signed 16-bit value from analog output 7
signed_value = jaka.read_sign16(ao_number=7)
print(f"Signed Analog Output 7 Value: {signed_value}")

# Read a 32-bit floating-point value from a specific register
float_value = jaka.read_float32(address=150)
print(f"Float Value at Register 150: {float_value}")
```

---

### Writing Analog Values

```python
# Write unsigned 16-bit integer to analog output 4
jaka.write_analog_output_int(ao_number=4, value=1234)

# Write signed 16-bit integer to analog output 6
jaka.write_analog_output_sign(ao_number=6, value=-123)

# Write a 32-bit floating-point value to analog output 2
jaka.write_analog_output_float32(ao_number=2, value=12.34)
```

---

### Reading Robot Status

```python
# Get joint 1 voltage
joint_voltage = jaka.get_joint_voltage(joint=1)
print(f"Joint 1 Voltage: {joint_voltage} V")

# Get joint 3 position
joint_position = jaka.get_joint_position(joint=3)
print(f"Joint 3 Position: {joint_position} degrees")

# Get joint 2 temperature
joint_temperature = jaka.get_joint_temperature(joint=2)
print(f"Joint 2 Temperature: {joint_temperature} °C")
```

---

### Monitoring Control Status

```python
# Check if the robot is powered on
is_powered_on = jaka.get_power_on_status()
print(f"Robot Powered On: {'Yes' if is_powered_on else 'No'}")

# Check if the robot is in position
in_position = jaka.get_inpos_status()
print(f"Robot In Position: {'Yes' if in_position else 'No'}")

# Get current movement mode
movement_mode = jaka.get_movement_mode()
print(f"Movement Mode: {movement_mode}")
```

---

### Exception Handling Example

```python
try:
    joint_speed = jaka.get_joint_speed(joint=1)
    print(f"Joint 1 Speed: {joint_speed} rad/s")
except Exception as e:
    print(f"Error reading joint speed: {e}")
```

---

### Closing the Connection

Always close the connection after completing operations:

```python
jaka.close()
```

---

## Full Example

```python
from JakaModbusCommunication import Jaka_Coms

# Connect to Jaka robot
jaka = Jaka_Coms(host="192.168.1.186", port=502)

try:
    # Read and print joint voltage
    voltage = jaka.get_joint_voltage(joint=1)
    print(f"Joint 1 Voltage: {voltage} V")

    # Set digital output 3 to ON
    jaka.write_digital_modbus_output(output_number=3, state=True)

    # Read position of joint 2
    position = jaka.get_joint_position(joint=2)
    print(f"Joint 2 Position: {position} degrees")

    # Write float value to analog output 1
    jaka.write_analog_output_float32(ao_number=1, value=15.67)
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    jaka.close()
```

---

This library makes it simple to integrate Jaka cobots into your automation systems. Ensure your Modbus TCP server is configured correctly for seamless operation.
