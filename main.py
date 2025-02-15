import pyautogui
import time
import cv2
import numpy as np

def run_in_circles():
    """Simulate running in circles to hatch eggs."""
    start_time = time.time()
    directions = ["right", "down", "left", "up"]  # Circular pattern

    try:
        while True:
            for direction in directions:
                if direction != "right" and direction != "left":
                    pyautogui.keyDown(direction)
                    time.sleep(2)  # Shorter key press
                    pyautogui.keyUp(direction)

                    # Check for egg hatch between movements
                    if detect_hatch():
                        print("Egg hatching detected! Stopping movement...")
                        pyautogui.press("z")
                        pyautogui.press("z")
                        time.sleep(10)
                        pyautogui.press("z")
                        pyautogui.press("z")
                        pyautogui.press("z")
                        print("press z u...")
                        return
    except KeyboardInterrupt:
        print("\nStopping script, releasing keys...")
    finally:
        for key in ["down", "up", "z"]:
            pyautogui.keyUp(key)

def detect_hatch(screen_region=(0, 670, 700, 200), hatch_template="test.png"):
    """Detect when an egg hatches using image recognition."""
    print("Checking for egg hatch screen...")
    screenshot = pyautogui.screenshot(region=screen_region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(hatch_template, cv2.IMREAD_GRAYSCALE)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val > 0.8  # Adjust threshold as needed

def main():
    """Main automation loop."""
    print("Starting Pokémon Egg Hatching Automation...")

    while True:
        run_in_circles()

if __name__ == "__main__":
    main()

# below is script to screenshot
# import pyautogui
# import os
# print(pyautogui.position())
# print(os.getcwd())
# image=pyautogui.screenshot("/Users/ridhoperdana/workspace/pokemonhatch/test.png", region=(0, 670, 700, 200))
# image.save('/Users/ridhoperdana/workspace/pokemonhatch/hatch.png')
