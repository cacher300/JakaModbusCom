import unittest
import sys
import types


pymodbus_module = types.ModuleType("pymodbus")
client_module = types.ModuleType("pymodbus.client")
exceptions_module = types.ModuleType("pymodbus.exceptions")


class StubModbusException(Exception):
    pass


class StubModbusTcpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        return True

    def is_socket_open(self):
        return False

    def close(self):
        return None


client_module.ModbusTcpClient = StubModbusTcpClient
exceptions_module.ModbusException = StubModbusException
pymodbus_module.client = client_module
pymodbus_module.exceptions = exceptions_module
sys.modules.setdefault("pymodbus", pymodbus_module)
sys.modules.setdefault("pymodbus.client", client_module)
sys.modules.setdefault("pymodbus.exceptions", exceptions_module)

from JakaModbusCommunication import Jaka_Coms


class FakeClient:
    def __init__(self):
        self.read_input_calls = []
        self.write_register_calls = []
        self.write_registers_calls = []
        self.closed = False

    def read_input_registers(self, address, count):
        self.read_input_calls.append((address, count))
        raise AssertionError("Unexpected Modbus read during this test")

    def write_register(self, address, value):
        self.write_register_calls.append((address, value))
        raise AssertionError("Unexpected Modbus write during this test")

    def write_registers(self, address, values):
        self.write_registers_calls.append((address, values))

        class Response:
            @staticmethod
            def isError():
                return False

        return Response()

    def is_socket_open(self):
        return not self.closed

    def close(self):
        self.closed = True


class JakaComsValidationTests(unittest.TestCase):
    def setUp(self):
        self.jaka = Jaka_Coms("127.0.0.1", auto_connect=False)
        self.jaka.client = FakeClient()

    def test_joint_validation_rejects_out_of_range_values(self):
        with self.assertRaises(ValueError):
            self.jaka.get_joint_voltage(0)

        with self.assertRaises(ValueError):
            self.jaka.get_joint_position(7)

    def test_tcp_axis_validation_rejects_invalid_axis(self):
        with self.assertRaises(ValueError):
            self.jaka.get_tcp_position("yaw")

    def test_tcp_axis_validation_accepts_lowercase_axis_names(self):
        addresses = []

        def fake_read_float32(address):
            addresses.append(address)
            return 1.23

        self.jaka.read_float32 = fake_read_float32

        value = self.jaka.get_tcp_speed("rz")

        self.assertEqual(value, 1.23)
        self.assertEqual(addresses, [428])

    def test_analog_output_validation_rejects_out_of_range_values(self):
        with self.assertRaises(ValueError):
            self.jaka.read_int16(0)

        with self.assertRaises(ValueError):
            self.jaka.write_analog_output_float32(17, 12.34)

    def test_write_analog_output_float32_uses_expected_register_address(self):
        self.jaka.write_analog_output_float32(2, 12.34)

        self.assertEqual(len(self.jaka.client.write_registers_calls), 1)
        address, values = self.jaka.client.write_registers_calls[0]
        self.assertEqual(address, 134)
        self.assertEqual(len(values), 2)


if __name__ == "__main__":
    unittest.main()
