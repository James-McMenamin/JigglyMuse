import unittest
from unittest.mock import patch, MagicMock
import time
from JigglyMuse import JigglyMuse

class TestJigglyMuse(unittest.TestCase):
    @patch('pyautogui.size')
    @patch('pyautogui.position')
    def setUp(self, mock_position, mock_size):
        mock_size.return_value = (1920, 1080)
        mock_position.return_value = (960, 540)
        self.jiggler = JigglyMuse()

    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    @patch('time.sleep')
    def test_simulate_reading(self, mock_sleep, mock_position, mock_moveTo):
        mock_position.return_value = (960, 540)
        self.jiggler.simulate_reading()
        mock_moveTo.assert_called_once()
        mock_sleep.assert_called_once()
        
    @patch('pyautogui.moveRel')
    @patch('pyautogui.position')
    @patch('keyboard.press')
    @patch('keyboard.release')
    @patch('time.sleep')
    def test_micro_movement(self, mock_sleep, mock_release, mock_press, 
                           mock_position, mock_moveRel):
        mock_position.return_value = (960, 540)
        self.jiggler.micro_movement()
        mock_moveRel.assert_called_once()
        
    @patch('keyboard.press')
    @patch('keyboard.release')
    @patch('time.sleep')
    def test_prevent_idle(self, mock_sleep, mock_release, mock_press):
        with patch('random.random', return_value=0.1):
            self.jiggler.prevent_idle()
            mock_press.assert_called_once()
            mock_release.assert_called_once()

    @patch('JigglyMuse.JigglyMuse.simulate_reading')
    @patch('JigglyMuse.JigglyMuse.micro_movement')
    @patch('JigglyMuse.JigglyMuse.prevent_idle')
    def test_run_work_hours(self, mock_prevent_idle, mock_micro, mock_reading):
        with patch('datetime.datetime') as mock_date:
            mock_date.now.return_value.hour = 14  # Work hours
            with patch('random.random', return_value=0.5):
                try:
                    # Run for a brief moment then simulate KeyboardInterrupt
                    with patch('time.sleep', side_effect=KeyboardInterrupt):
                        self.jiggler.run()
                except KeyboardInterrupt:
                    pass
                
                mock_reading.assert_called()
                mock_prevent_idle.assert_called()

    def test_initialization(self):
        self.assertEqual(self.jiggler.screen_width, 1920)
        self.assertEqual(self.jiggler.screen_height, 1080)
        self.assertEqual(self.jiggler.reading_direction, 1)
        self.assertListEqual(self.jiggler.safe_keys, ['shift', 'alt', 'ctrl'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
