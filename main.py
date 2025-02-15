import pyautogui
import time
import cv2
import numpy as np
import pytesseract
import requests
from io import BytesIO

def ocr_api_request(image_data):
    """Send image to OCR API and return extracted text."""
    url = "https://ocr-llm.arshadyaseen.com/api/extract"
    files = {'images': ('image.png', BytesIO(image_data), 'image/png')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json().get("results", [{}])[0].get("content", "")
    return ""

def detect_egg_text_via_api():
    """Detect if 'Egg' is present using the OCR API."""
    start_time = time.time()
    print("detect egg via API...")
    screenshot = screenshot_retroarch()
    if screenshot is None:
        return False
    processed_image = preprocess_image(screenshot)
    _, image_encoded = cv2.imencode('.png', processed_image)
    extracted_text = ocr_api_request(image_encoded.tobytes())
    elapsed_time = time.time() - start_time
    print(f"detect_egg_text_via_api took {elapsed_time:.4f} seconds")
    print("OCR API Output:", extracted_text)
    return "Egg" in extracted_text

def screenshot_retroarch():
    """Capture a screenshot of the RetroArch window only."""
    start_time = time.time()
    print("Capturing screenshot...")
    ss = pyautogui.screenshot()
    print("Capturing screenshot Done...")
    elapsed_time = time.time() - start_time
    print(f"screenshot_retroarch took {elapsed_time:.4f} seconds")
    return np.array(ss)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    upscaled = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    binary = cv2.threshold(upscaled, 150, 255, cv2.THRESH_BINARY_INV)[1]
    return binary

def detect_egg_text():
    """Check if the word 'Egg' is visible in the inventory."""
    print("Detecting Egg text...")
    screenshot = screenshot_retroarch()
    if screenshot is None:
        return False

    processed_image = preprocess_image(screenshot)

    print("Processing Egg text...")
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(processed_image)

    print(f"Detecting Egg text... f{text}")

    # Check if "Egg" appears in the extracted text
    return "Egg" in text

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
                        time.sleep(7)
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
        pyautogui.press("return")
        time.sleep(1)
        pyautogui.press("x")
        time.sleep(3)
        if detect_egg_text_via_api() is not True:
            print("Egg not exists anymore. Stopping script...")
            break
        else:
            pyautogui.press("z")
            time.sleep(3)
            pyautogui.press("z")
            time.sleep(1)


if __name__ == "__main__":
    main()
