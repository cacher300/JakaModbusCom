"""
Jaka_Coms.py

This module provides a ModbusHelper class to read discrete input states
from a Modbus TCP server. The input numbering is mapped such that:
- Input 1 corresponds to Modbus address 8.
- Input N corresponds to Modbus address 7 + N.

"""
import struct

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException


class Jaka_Coms:
    def __init__(self, host: str, port: int = 502, auto_connect: bool = True):
        """
        Initialize the ModbusHelper.

        :param host: IP address or hostname of the Modbus TCP server.
        :param port: Modbus TCP port (default: 502).
        :param auto_connect: Whether to automatically connect upon instantiation.
        """
        self.host = host
        self.port = port
        self.client = ModbusTcpClient(host=self.host, port=self.port)

        if auto_connect:
            self.connect()

    def connect(self) -> bool:
        """
        Establishes a connection to the Modbus TCP server.

        :return: True if connection is successful, False otherwise.
        """
        try:
            if self.client.connect():
                print(f"Connected to Modbus server at {self.host}:{self.port}")
                return True
            else:
                print(f"Unable to connect to Modbus server at {self.host}:{self.port}")
                return False
        except ModbusException as e:
            print(f"Modbus connection error: {e}")
            return False

    def close(self):
        """
        Closes the connection to the Modbus TCP server.
        """
        self.client.close()
        print("Closed connection to Modbus server.")

    def read_modbus_input_state(self, input_number: int) -> bool:
        """
        Reads the state of a single discrete input.

        Input mapping:
        - Input 1 corresponds to Modbus address 8.
        - Input N corresponds to Modbus address 7 + N.

        :param input_number: The input number (1 to 128).
        :return: Boolean state of the input (True or False).
        :raises ValueError: If input_number is outside the valid range.
        :raises ModbusException: If the read operation fails.
        """
        if not (1 <= input_number <= 128):
            raise ValueError("input_number must be between 1 and 128.")

        address = 7 + input_number
        response = self.client.read_discrete_inputs(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading input {input_number} at address {address}: {response}")

        return response.bits[0]

    def read_jaka_cab_input_state_mini(self, input_number: int) -> bool:
        """
        Reads the state of a discrete input specific to JAKA CAB MINI.

        :param input_number: The input number (1 to 7).
        :return: Boolean state of the input (True or False).
        :raises ValueError: If input_number is outside the valid range.
        :raises ModbusException: If the read operation fails.
        """
        if not (1 <= input_number <= 7):
            raise ValueError("input_number must be between 1 and 7.")

        address = 135 + input_number
        response = self.client.read_discrete_inputs(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading input {input_number} at address {address}: {response}")

        return response.bits[0]

    def read_jaka_cab_input_state_zu(self, input_number: int) -> bool:
        """
        Reads the state of a discrete input specific to JAKA CAB ZU.

        :param input_number: The input number (1 to 16).
        :return: Boolean state of the input (True or False).
        :raises ValueError: If input_number is outside the valid range.
        :raises ModbusException: If the read operation fails.
        """
        if not (1 <= input_number <= 16):
            raise ValueError("input_number must be between 1 and 16.")

        address = 135 + input_number
        response = self.client.read_discrete_inputs(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading input {input_number} at address {address}: {response}")

        return response.bits[0]

    def read_jaka_tool_input_state(self, input_number: int) -> bool:
        """
        Reads the state of a discrete input specific to JAKA TOOL.

        :param input_number: The input number (1 to 2).
        :return: Boolean state of the input (True or False).
        :raises ValueError: If input_number is outside the valid range.
        :raises ModbusException: If the read operation fails.
        """
        if not (1 <= input_number <= 2):
            raise ValueError("input_number must be between 1 and 2.")

        address = 151 + input_number
        response = self.client.read_discrete_inputs(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading input {input_number} at address {address}: {response}")

        return response.bits[0]

    def read_int16(self, ao_number: int) -> int:
        """
        Reads a UINT16 value from the given analog output.

        :param ao_number: The analog output number (1 to 16).
        :return: Unsigned 16-bit integer value.
        :raises ModbusException: If the read operation fails.
        """
        address = 95 + ao_number
        response = self.client.read_input_registers(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading UINT16 AO{ao_number} at address {address}")

        return response.registers[0]

    def read_sign16(self, ao_number: int) -> int:
        """
        Reads a signed INT16 value from the given analog output.

        :param ao_number: The analog output number (1 to 16).
        :return: Signed 16-bit integer value.
        :raises ModbusException: If the read operation fails.
        """
        address = 111 + ao_number - 16
        response = self.client.read_input_registers(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading INT16 AO{ao_number} at address {address}")

        value = response.registers[0] if response.registers[0] < 32768 else response.registers[0] - 65536
        return value

    def read_float32(self, address: int) -> float:
        """
        Reads a 32-bit floating-point value from the specified address.

        :param address: The Modbus register address to read from.
        :return: 32-bit floating-point value.
        :raises ModbusException: If the read operation fails.
        """
        response = self.client.read_input_registers(address=address, count=2)

        if response.isError():
            raise ModbusException(f"Error reading FLOAT32 value at address {address}")

        raw = struct.pack(">HH", response.registers[0], response.registers[1])
        return struct.unpack(">f", raw)[0]

    def write_digital_modbus_output(self, output_number: int, state: bool):
        """
        Writes a state (ON/OFF) to a digital output (coil).

        :param output_number: The digital output number (1 to 128).
        :param state: Desired state (True for ON, False for OFF).
        :raises ValueError: If output_number is not within the valid range.
        :raises ModbusException: If the write operation fails.
        """
        if not (1 <= output_number <= 128):
            raise ValueError("output_number must be between 1 and 128.")

        address = 39 + output_number
        response = self.client.write_coil(address=address, value=state)

        if response.isError():
            raise ModbusException(f"Error writing to digital output {output_number} at address {address}")

    def write_digital_cab_mini_output(self, output_number: int, state: bool):
        """
        Writes a state (ON/OFF) to a digital output specific to JAKA CAB MINI.

        :param output_number: The output number (1 to 7).
        :param state: Desired state (True for ON, False for OFF).
        :raises ValueError: If output_number is not within the valid range.
        :raises ModbusException: If the write operation fails.
        """
        if not (1 <= output_number <= 7):
            raise ValueError("output_number must be between 1 and 7.")

        address = 167 + output_number
        response = self.client.write_coil(address=address, value=state)

        if response.isError():
            raise ModbusException(f"Error writing to digital output {output_number} at address {address}")

    def write_analog_output_int(self, ao_number: int, value: int):
        """
        Writes an unsigned 16-bit integer value to an analog output.

        :param ao_number: The analog output number (1 to 16).
        :param value: The unsigned 16-bit integer value to write.
        :raises ValueError: If ao_number is not within the valid range.
        :raises ModbusException: If the write operation fails.
        """
        if not (1 <= ao_number <= 16):
            raise ValueError("ao_number must be between 1 and 16.")

        address = 99 + ao_number
        response = self.client.write_register(address=address, value=value)

        if response.isError():
            raise ModbusException(f"Error writing UINT16 value to AO{ao_number} at address {address}")

    def write_analog_output_float32(self, ao_number: int, value: float):
        """
        Writes a 32-bit floating-point value to an analog output.

        :param ao_number: The analog output number (1 to 16).
        :param value: The floating-point value to write.
        :raises ValueError: If ao_number is not within the valid range.
        :raises ModbusException: If the write operation fails.
        """
        ao_number = 2 * (ao_number - 1) + 1
        address = 131 + ao_number

        # Pack the float value into two 16-bit registers (big-endian)
        raw = struct.pack(">f", value)
        registers = struct.unpack(">HH", raw)

        # Write the two 16-bit registers to the Modbus server
        response = self.client.write_registers(address=address, values=list(registers))

        if response.isError():
            raise ModbusException(f"Error writing FLOAT32 value to AO{ao_number} at address {address}")

    def write_analog_output_sign(self, ao_number: int, value: int):
        """
        Writes a signed 16-bit integer value to an analog output.

        :param ao_number: The analog output number (1 to 16).
        :param value: The signed 16-bit integer value to write.
        :raises ValueError: If ao_number is not within the valid range.
        :raises ModbusException: If the write operation fails.
        """
        if not (1 <= ao_number <= 16):
            raise ValueError("ao_number must be between 1 and 16.")

        address = 115 + ao_number
        response = self.client.write_register(address=address, value=value)

        if response.isError():
            raise ModbusException(f"Error writing INT16 value to AO{ao_number} at address {address}")

    def read_uint16(self, address: int) -> int:
        """
        Reads an unsigned 16-bit integer value from the specified address.

        :param address: The Modbus register address to read from.
        :return: Unsigned 16-bit integer value.
        :raises ModbusException: If the read operation fails.
        """
        response = self.client.read_input_registers(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading UINT16 value at address {address}")

        return response.registers[0]

    def read_int32(self, address: int) -> int:
        """
        Reads a 32-bit signed integer value from the specified address.

        :param address: The Modbus register address to read from.
        :return: Signed 32-bit integer value.
        :raises ModbusException: If the read operation fails.
        """
        response = self.client.read_input_registers(address=address, count=2)

        if response.isError():
            raise ModbusException(f"Error reading INT32 value at address {address}")

        # Combine two 16-bit registers into a 32-bit signed integer (big-endian)
        raw = struct.pack(">HH", response.registers[0], response.registers[1])
        return struct.unpack(">i", raw)[0]  # Interpret as signed 32-bit integer

    # Servo and Serial Data
    def get_servo_version(self) -> int:
        """
        Retrieves the servo version from the robot.

        :return: Servo version as an integer.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_int32(300)

    def get_robot_serial_no(self) -> int:
        """
        Retrieves the serial number of the robot.

        :return: Robot serial number as an integer.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_int32(302)

    # Joint Voltages
    def get_joint_voltage(self, joint: int) -> float:
        """
        Retrieves the voltage of a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Joint voltage in float.
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(304 + (joint - 1) * 2)

    # Joint Temperatures
    def get_joint_temperature(self, joint: int) -> float:
        """
        Retrieves the temperature of a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Joint temperature in float.
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(316 + (joint - 1) * 2)

    # Joint Servo Error Code
    def get_joint_servo_error_code(self, joint: int) -> int:
        """
        Retrieves the servo error code for a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Servo error code as an integer.
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_int32(328 + (joint - 1) * 2)

    # Joint Error Status
    def get_joint_error_status(self, joint: int) -> int:
        """
        Retrieves the error status for a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Error status as an integer.
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(340 + (joint - 1))

    # Joint Enabled Status
    def get_joint_enabled_status(self, joint: int) -> int:
        """
        Checks whether a specified joint is enabled.

        :param joint: Joint number (1 to 6).
        :return: Enabled status (1 for enabled, 0 for disabled).
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(346 + (joint - 1))

    # Joint Collision Status
    def get_joint_collision_status(self, joint: int) -> int:
        """
        Checks the collision status of a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Collision status (1 for collision detected, 0 otherwise).
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(352 + (joint - 1))

    # Joint Currents
    def get_joint_current(self, joint: int) -> float:
        """
        Retrieves the current of a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Joint current in float.
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return abs(self.read_float32(358 + (joint - 1) * 2))

    # Joint Position
    def get_joint_position(self, joint: int) -> float:
        """
        Retrieves the position of a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Joint position in float.
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(382 + (joint - 1) * 2)

    # Joint Speed
    def get_joint_speed(self, joint: int) -> float:
        """
        Retrieves the speed of a specified joint.

        :param joint: Joint number (1 to 6).
        :return: Joint speed in float.
        :raises ValueError: If the joint number is invalid.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(394 + (joint - 1) * 2)

    # TCP Position
    def get_tcp_position(self, axis: str) -> float:
        """
        Retrieves the TCP (tool center point) position for a specified axis.

        :param axis: Axis name (X, Y, Z, RX, RY, RZ).
        :return: TCP position along the specified axis in float.
        :raises KeyError: If the axis is invalid.
        :raises ModbusException: If the read operation fails.
        """
        axis_mapping = {"X": 406, "Y": 408, "Z": 410, "RX": 412, "RY": 414, "RZ": 416}
        return self.read_float32(axis_mapping[axis])

    # TCP Speed
    def get_tcp_speed(self, axis: str) -> float:
        """
        Retrieves the TCP (tool center point) speed for a specified axis.

        :param axis: Axis name (X, Y, Z, RX, RY, RZ).
        :return: TCP speed along the specified axis in float.
        :raises KeyError: If the axis is invalid.
        :raises ModbusException: If the read operation fails.
        """
        axis_mapping = {"X": 418, "Y": 420, "Z": 422, "RX": 424, "RY": 426, "RZ": 428}
        return self.read_float32(axis_mapping[axis])

    # Control Status
    def get_collision_protective_stop(self) -> int:
        """
        Checks if a collision protective stop is active.

        :return: 1 if active, 0 otherwise.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(454)

    def get_emergency_stop(self) -> int:
        """
        Checks if an emergency stop is active.

        :return: 1 if active, 0 otherwise.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(455)

    def get_power_on_status(self) -> int:
        """
        Checks if the robot is powered on.

        :return: 1 if powered on, 0 otherwise.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(456)

    def get_robot_enable_status(self) -> int:
        """
        Checks if the robot is enabled.

        :return: 1 if enabled, 0 otherwise.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(457)

    def get_on_soft_limit(self) -> int:
        """
        Checks if the robot is on a soft limit.

        :return: 1 if on soft limit, 0 otherwise.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(458)

    def get_inpos_status(self) -> int:
        """
        Checks if the robot is in position.

        :return: 1 if in position, 0 otherwise.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(459)

    def get_movement_mode(self) -> int:
        """
        Retrieves the current movement mode of the robot.

        :return: Movement mode as an integer.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(460)

    def get_percentage_mode_level(self) -> int:
        """
        Retrieves the percentage mode level of the robot.

        :return: Percentage mode level as an integer.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(461)

    def get_speed_magnification(self) -> float:
        """
        Retrieves the speed magnification factor.

        :return: Speed magnification as a float.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(462)

    # Cabinet Data
    def get_cab_temperature(self) -> float:
        """
        Retrieves the cabinet temperature.

        :return: Cabinet temperature in float.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(466)

    def get_cab_average_power(self) -> float:
        """
        Retrieves the average power consumption of the cabinet.

        :return: Average power in float.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(468)

    def get_cab_average_current(self) -> float:
        """
        Retrieves the average current consumption of the cabinet.

        :return: Average current in float.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(470)

    # Error Data
    def get_motion_error_code(self) -> int:
        """
        Retrieves the motion error code.

        :return: Motion error code as an integer.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_int32(464)

    def get_error_triggered(self) -> int:
        """
        Checks if an error has been triggered.

        :return: 1 if error triggered, 0 otherwise.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(479)

    # UHI Conveyor Data
    def get_uhi_pulse(self) -> float:
        """
        Retrieves the UHI conveyor pulse count.

        :return: Pulse count in float.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(472)

    def get_uhi_speed(self) -> float:
        """
        Retrieves the UHI conveyor speed.

        :return: Speed in float.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_float32(474)

    def get_uhi_direction(self) -> int:
        """
        Retrieves the UHI conveyor direction.

        :return: 1 for forward, 0 for reverse.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_uint16(476)

    def get_uhi_origin_pulse(self) -> int:
        """
        Retrieves the UHI origin pulse.

        :return: Origin pulse as an integer.
        :raises ModbusException: If the read operation fails.
        """
        return self.read_int32(477)

    def __del__(self):
        """
        Destructor to ensure connection is closed if the object is garbage-collected.
        """
        if self.client.is_socket_open():
            self.close()
