import pyautogui
import random
import time
import sys
import math
from datetime import datetime
import keyboard

class JigglyMuse:
    def __init__(self):
        # Disable pyautogui's failsafe
        pyautogui.FAILSAFE = False
        # Get screen size
        self.screen_width, self.screen_height = pyautogui.size()
        # Initialize last position and time
        self.last_x, self.last_y = pyautogui.position()
        self.last_move_time = time.time()
        # Track reading patterns
        self.reading_direction = 1  # 1 for down, -1 for up
        # Add common modifier keys that won't trigger anything when pressed
        self.safe_keys = ['shift', 'alt', 'ctrl']
        
    def simulate_reading(self):
        """Simulate natural reading patterns"""
        current_x, current_y = pyautogui.position()
        
        # Subtle vertical movement like reading
        scroll_amount = random.uniform(0.5, 2.0) * self.reading_direction
        new_y = current_y + scroll_amount
        
        # Change direction if we've gone too far
        if new_y > self.screen_height * 0.8:
            self.reading_direction = -1
        elif new_y < self.screen_height * 0.2:
            self.reading_direction = 1
            
        # Occasionally add tiny horizontal shifts
        new_x = current_x + random.uniform(-1, 1)
        
        # Super slow movement
        pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.3, 0.8))
        
        # Variable pause to simulate reading
        time.sleep(random.uniform(2.0, 5.0))

    def micro_movement(self):
        """Tiny, barely noticeable movements"""
        current_x, current_y = pyautogui.position()
        offset_x = random.uniform(-0.5, 0.5)
        offset_y = random.uniform(-0.5, 0.5)
        pyautogui.moveRel(offset_x, offset_y, duration=0.3)
        
        # Simulate subtle keyboard activity
        if random.random() < 0.2:  # 20% chance
            random_key = random.choice(self.safe_keys)
            keyboard.press(random_key)
            time.sleep(0.1)
            keyboard.release(random_key)
            
        time.sleep(random.uniform(3.0, 7.0))

    def prevent_idle(self):
        """Specific anti-idle actions for chat apps"""
        if random.random() < 0.15:  # 15% chance
            # Press and release a modifier key (won't trigger any actions)
            key = random.choice(self.safe_keys)
            keyboard.press(key)
            time.sleep(0.1)
            keyboard.release(key)
            
            # Teams/Slack often check for keyboard activity
            time.sleep(0.2)

    def run(self):
        print("JigglyMuse is silently keeping you active... (Ctrl+C to stop)")
        
        try:
            while True:
                # Get current hour
                hour = datetime.now().hour
                
                # During work hours, be more active
                if 8 <= hour <= 18:  # Extended work hours
                    if random.random() < 0.7:
                        self.simulate_reading()
                    else:
                        self.micro_movement()
                    
                    # Extra anti-idle measures during work hours
                    self.prevent_idle()
                else:
                    self.micro_movement()
                    
                # Randomize activity to seem more human
                if random.random() < 0.1:
                    time.sleep(random.uniform(15, 45))  # Longer breaks
                
        except KeyboardInterrupt:
            print("\nStopping...")

if __name__ == "__main__":
    jiggler = JigglyMuse()
    jiggler.run()
