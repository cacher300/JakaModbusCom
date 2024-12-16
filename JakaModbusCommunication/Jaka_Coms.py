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
        Jaka output state
        Modbus Input
        Reads the state of a single discrete input. Input 1 is mapped to
        Modbus address 8, input 2 to address 9, etc.

        :param input_number: The input number (1 to 128).
        :return: Boolean state of the input (True / False).
        :raises ValueError: If input_number is outside the valid range.
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
        Jaka cab input state

        :param input_number: The input number (1 to 128).
        :return: Boolean state of the input (True / False).
        :raises ValueError: If input_number is outside the valid range.
        """
        if not (1 <= input_number <= 7):
            raise ValueError("input_number must be between 1 and 128.")

        address = 135 + input_number
        response = self.client.read_discrete_inputs(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading input {input_number} at address {address}: {response}")

        return response.bits[0]

    def read_jaka_cab_input_state_zu(self, input_number: int) -> bool:
        """
        Jaka cab input state

        :param input_number: The input number (1 to 128).
        :return: Boolean state of the input (True / False).
        :raises ValueError: If input_number is outside the valid range.
        """
        if not (1 <= input_number <= 16):
            raise ValueError("input_number must be between 1 and 128.")

        address = 135 + input_number
        response = self.client.read_discrete_inputs(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading input {input_number} at address {address}: {response}")

        return response.bits[0]

    def read_jaka_tool_input_state(self, input_number: int) -> bool:
        """
        Jaka tool input state


        :param input_number: The input number (1 to 128).
        :return: Boolean state of the input (True / False).
        :raises ValueError: If input_number is outside the valid range.
        """
        if not (1 <= input_number <= 2):
            raise ValueError("input_number must be between 1 and 128.")

        address = 151 + input_number
        response = self.client.read_discrete_inputs(address=address, count=1)

        if response.isError():
            raise ModbusException(f"Error reading input {input_number} at address {address}: {response}")

        return response.bits[0]

    def read_int16(self, ao_number: int) -> int:
        """
        Reads the UINT16 value for the given AO number.
        """
        address = 95 + ao_number
        response = self.client.read_input_registers(address=address, count=1)
        if response.isError():
            raise ModbusException(f"Error reading UINT16 AO{ao_number} at address {address}")
        print(f"AO{ao_number} (UINT16) Value: {response.registers[0]}")
        return response.registers[0]

    def read_sign16(self, ao_number: int) -> int:
        """
        Reads the INT16 value for the given AO number.
        """
        address = 111 + ao_number -16
        response = self.client.read_input_registers(address=address, count=1)
        if response.isError():
            raise ModbusException(f"Error reading INT16 AO{ao_number} at address {address}")
        value = response.registers[0] if response.registers[0] < 32768 else response.registers[0] - 65536
        print(f"AO{ao_number} (INT16) Value: {value}")
        return value

    def read_float32(self, ao_number: int) -> float:
        """
        Reads the FLOAT32 value for the given AO number.
        """
        ao_number = 2 * ao_number - 1
        print(ao_number)
        address = 127 + ao_number
        response = self.client.read_input_registers(address=address, count=2)
        print(response)
        if response.isError():
            raise ModbusException(f"Error reading FLOAT32 AO{ao_number} at address {address}")
        raw = struct.pack(">HH", response.registers[0], response.registers[1])
        value = struct.unpack(">f", raw)[0]
        print(f"AO{ao_number} (FLOAT32) Value: {value}")
        return value

    def write_digital_modbus_output(self, output_number: int, state: bool):
        """
        Writes a state (ON/OFF) to a digital output (coil).

        :param output_number: The digital output number (CAB DO or TOOL DO).
        :param state: True for ON, False for OFF.
        """
        if not (1 <= output_number <= 128):
            raise ValueError("input_number must be between 1 and 128.")
        address = 39 + output_number
        response = self.client.write_coil(address=address, value=state)

        if response.isError():
            raise ModbusException(f"Error writing to digital output {output_number} at address {address}")
        print(f"Digital Output {output_number} set to {'ON' if state else 'OFF'}.")

    def write_digital_cab_mini_output(self, output_number: int, state: bool):
        """
        Writes a state (ON/OFF) to a digital output (coil).

        :param output_number: The digital output number (CAB DO or TOOL DO).
        :param state: True for ON, False for OFF.
        """
        if not (1 <= output_number <= 7):
            raise ValueError("input_number must be between 1 and 128.")
        address = 167 + output_number
        response = self.client.write_coil(address=address, value=state)

        if response.isError():
            raise ModbusException(f"Error writing to digital output {output_number} at address {address}")
        print(f"Digital Output {output_number} set to {'ON' if state else 'OFF'}.")


    def write_analog_output_int(self, ao_number: int, value: int):
        """
        Writes a UINT16 value to an Analog Output.
        """
        if not (1 <= ao_number <= 16):
            raise ValueError("input_number must be between 1 and 128.")
        address = 99 +ao_number
        response = self.client.write_register(address=address, value=value)
        if response.isError():
            raise ModbusException(f"Error writing UINT16 value to AO{ao_number} at address {address}")
        print(f"AO{ao_number} (UINT16) set to {value}.")

    def write_analog_output_float32(self, ao_number: int, value: float):
        """
        Writes a FLOAT32 value to an Analog Output.

        :param ao_number: The Analog Output number (e.g., A132–A164).
        :param value: The FLOAT32 value to write.
        """
        ao_number = 2 * (ao_number - 1) + 1
        address = 131 + ao_number
        print(f"Writing FLOAT32 value {value} to AO{ao_number} at address {address}...")

        # Pack the float value into two 16-bit registers (big-endian)
        raw = struct.pack(">f", value)
        registers = struct.unpack(">HH", raw)

        # Write the two 16-bit registers to the Modbus server
        response = self.client.write_registers(address=address, values=list(registers))
        if response.isError():
            raise ModbusException(f"Error writing FLOAT32 value to AO{ao_number} at address {address}")

        print(f"Successfully wrote FLOAT32 value {value} to AO{ao_number}.")

    def write_analog_output_sign(self, ao_number: int, value: int):
        """
        Writes a UINT16 value to an Analog Output.
        """
        if not (1 <= ao_number <= 16):
            raise ValueError("input_number must be between 1 and 128.")
        address = 115 + ao_number
        response = self.client.write_register(address=address, value=value)
        if response.isError():
            raise ModbusException(f"Error writing UINT16 value to AO{ao_number} at address {address}")
        print(f"AO{ao_number} (UINT16) set to {value}.")

        # Servo and Serial Data
        def get_servo_version(self) -> int:
            return self.read_int32(300)

        def get_robot_serial_no(self) -> int:
            return self.read_int32(302)

        # Joint Voltages
        def get_joint_voltage(self, joint: int) -> float:
            return self.read_float32(304 + (joint - 1) * 2)

        # Joint Temperatures
        def get_joint_temperature(self, joint: int) -> float:
            return self.read_float32(316 + (joint - 1) * 2)

        # Joint Servo Error Code
        def get_joint_servo_error_code(self, joint: int) -> int:
            return self.read_int32(328 + (joint - 1) * 2)

        # Joint Error Status
        def get_joint_error_status(self, joint: int) -> int:
            return self.read_uint16(340 + (joint - 1))

        # Joint Enabled Status
        def get_joint_enabled_status(self, joint: int) -> int:
            return self.read_uint16(346 + (joint - 1))

        # Joint Collision Status
        def get_joint_collision_status(self, joint: int) -> int:
            return self.read_uint16(352 + (joint - 1))

        # Joint Currents
        def get_joint_current(self, joint: int) -> float:
            return self.read_float32(358 + (joint - 1) * 2)

        # Joint Position
        def get_joint_position(self, joint: int) -> float:
            return self.read_float32(382 + (joint - 1) * 2)

        # Joint Speed
        def get_joint_speed(self, joint: int) -> float:
            return self.read_float32(394 + (joint - 1) * 2)

        # TCP Position
        def get_tcp_position(self, axis: str) -> float:
            axis_mapping = {"X": 406, "Y": 408, "Z": 410, "RX": 412, "RY": 414, "RZ": 416}
            return self.read_float32(axis_mapping[axis])

        # TCP Speed
        def get_tcp_speed(self, axis: str) -> float:
            axis_mapping = {"X": 418, "Y": 420, "Z": 422, "RX": 424, "RY": 426, "RZ": 428}
            return self.read_float32(axis_mapping[axis])

        # Control Status
        def get_collision_protective_stop(self) -> int:
            return self.read_uint16(454)

        def get_emergency_stop(self) -> int:
            return self.read_uint16(455)

        def get_power_on_status(self) -> int:
            return self.read_uint16(456)

        def get_robot_enable_status(self) -> int:
            return self.read_uint16(457)

        def get_on_soft_limit(self) -> int:
            return self.read_uint16(458)

        def get_inpos_status(self) -> int:
            return self.read_uint16(459)

        def get_movement_mode(self) -> int:
            return self.read_uint16(460)

        def get_percentage_mode_level(self) -> int:
            return self.read_uint16(461)

        def get_speed_magnification(self) -> float:
            return self.read_float32(462)

        # Cabinet Data
        def get_cab_temperature(self) -> float:
            return self.read_float32(466)

        def get_cab_average_power(self) -> float:
            return self.read_float32(468)

        def get_cab_average_current(self) -> float:
            return self.read_float32(470)

        # Error Data
        def get_motion_error_code(self) -> int:
            return self.read_int32(464)

        def get_error_triggered(self) -> int:
            return self.read_uint16(479)

        # UHI Conveyor Data
        def get_uhi_pulse(self) -> float:
            return self.read_float32(472)

        def get_uhi_speed(self) -> float:
            return self.read_float32(474)

        def get_uhi_direction(self) -> int:
            return self.read_uint16(476)

        def get_uhi_origin_pulse(self) -> int:
            return self.read_int32(477)

    def __del__(self):
        """
        Destructor to ensure connection is closed if the object is garbage-collected.
        """
        if self.client.is_socket_open():
            self.close()
