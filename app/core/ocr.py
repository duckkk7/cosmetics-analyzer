import numpy as np
import cv2
import pytesseract
from app.core.utils import clean_and_merge_ingredients
import platform
import os

print("Файл существует?", os.path.exists(r"C:\Users\Vlada\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"))

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Vlada\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def ocr_image(image_bytes: bytes):

    nparr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(nparr, cv2.COLOR_BGR2GRAY)

    # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config, lang='eng')

    detected_texts = [line.strip() for line in text.split('\n') if line.strip()]

    ingredients = clean_and_merge_ingredients(detected_texts)

    print(f"\nбыло считано строк: {len(detected_texts)} => стало чистых ингредиентов: {len(ingredients)}")
    print("\nчистый список ингредиентов:")
    for i, ing in enumerate(ingredients, 1):
        print(f"{i:2}. {ing}")

    return ingredients
