import unittest
from unittest.mock import patch, MagicMock, call

from mock import max30102, GPIO
from src.smart_bedside_error import SmartBedsideError
from src.smart_bedside_system import SmartBedsideSystem


##########################################################################################
########################### Acceptance Tests for User Story #6 ###########################
##########################################################################################

class TestUserStory6(unittest.TestCase):

    @patch.object(max30102.DFRobot_BloodOxygen_S, "__init__", return_value=None)
    @patch.object(max30102.DFRobot_BloodOxygen_S, "begin")
    @patch.object(max30102.DFRobot_BloodOxygen_S, "sensor_start_collect")
    def test_spo2_sensor_initialization(self, mock_sensor_start_collect: MagicMock,
                                        mock_begin: MagicMock, mock_DFRobot_BloodOxygen_S: MagicMock):
        system = SmartBedsideSystem()
        # Assert that the sensor was instantiated without any arguments.
        mock_DFRobot_BloodOxygen_S.assert_called_once_with()
        # Assert that the sensor's begin() method was called exactly once.
        mock_begin.assert_called_once_with()
        # Assert that the sensor's data acquisition was started exactly once.
        mock_sensor_start_collect.assert_called_once_with()
        # Assert that the sensor was stored in the spo2_hr_sensor instance variable.
        self.assertIsInstance(system.spo2_hr_sensor, max30102.DFRobot_BloodOxygen_S)

    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_heartbeat")
    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_spo2")
    def test_read_valid_vital_signs(self, mock_get_spo2: MagicMock, mock_get_heartbeat: MagicMock):
        mock_get_spo2.return_value = 98  # Simulate a valid SpO2 reading of 98%.
        mock_get_heartbeat.return_value = 72  # Simulate a valid heart rate reading of 72 BPM.
        system = SmartBedsideSystem()
        vital_signs = system.read_vital_signs()
        # Assert that the returned list contains the SpO2 and the heart rate, in this order.
        self.assertEqual(vital_signs, [98, 72])

    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_heartbeat")
    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_spo2")
    def test_read_invalid_heart_rate(self, mock_get_spo2: MagicMock, mock_get_heartbeat: MagicMock):
        mock_get_spo2.return_value = 98  # Simulate a valid SpO2 reading of 98%.
        mock_get_heartbeat.return_value = -1  # Simulate an invalid heart rate reading.
        system = SmartBedsideSystem()
        # Assert that SmartBedsideError is raised when the sensor returns -1 for the heart rate.
        self.assertRaises(SmartBedsideError, system.read_vital_signs)

    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_heartbeat")
    @patch.object(max30102.DFRobot_BloodOxygen_S, "get_spo2")
    def test_read_invalid_spo2(self, mock_get_spo2: MagicMock, mock_get_heartbeat: MagicMock):
        mock_get_spo2.return_value = -1  # Simulate an invalid SpO2 reading.
        mock_get_heartbeat.return_value = 72  # Simulate a valid heart rate reading of 72 BPM.
        system = SmartBedsideSystem()
        # Assert that SmartBedsideError is still raised when the sensor returns -1 for the SpO2.
        self.assertRaises(SmartBedsideError, system.read_vital_signs)

##########################################################################################
######################## Run the acceptance tests of ALL user stories ####################
##########################################################################################

if __name__ == "__main__":
    unittest.main()
