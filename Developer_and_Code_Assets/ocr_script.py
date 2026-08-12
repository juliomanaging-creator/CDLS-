import sys
import cv2
import pytesseract
import pandas as pd
import os

# Set Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def run_ocr(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    
    # Just print to stdout so Node.js can read it
    print(f"EXTRACTED DATA: {text[:100]}...")
    
    # LOGIC: Append to your main CSV for the MCMC sim
    # (Use your existing regex patterns here to save to the CSV)
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_ocr(sys.argv[1])