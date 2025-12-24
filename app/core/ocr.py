import easyocr

from app.core.utils import clean_and_merge_ingredients

reader = easyocr.Reader(['en'], gpu=True)


def ocr_image(image):
    results = reader.readtext(image, detail=1)
    detected_texts = [text for (_, text, prob) in results if prob > 0.3]  # фильтр по уверенности
    ingredients = clean_and_merge_ingredients(detected_texts)

    # для дебага оставим пока
    print(f"\nбыло считано строк: {len(detected_texts)} => стало чистых ингредиентов: {len(ingredients)}")
    print("\nчистый список ингредиентов:")
    for i, ing in enumerate(ingredients, 1):
        print(f"{i:2}. {ing}")
    # удалить потом

    return ingredients
