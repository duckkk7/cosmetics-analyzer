import re


def clean_and_merge_ingredients(raw_lines):
    # объединяем всё в одну строку
    full_text = " ".join(raw_lines)
    # убираем типичный мусор (слово состав, воду)
    full_text = re.sub(r'\bIngredients?\b.*?(?=[A-Z]|$)', '', full_text, flags=re.I)
    full_text = re.sub(r'\bWater\s*\(?\s*Aqua\s*\)?\s*[;,]?\s*', '', full_text, flags=re.I)
    full_text = re.sub(r'\baqua\b', '', full_text, flags=re.I)

    # убираем переносы слов через дефис
    full_text = re.sub(r'\s*-\s*', '', full_text)
    # заменяем ВСЕ разделители на один: ";"
    full_text = re.sub(r'[;,]\s*', ';', full_text)
    # убираем лишние пробелы
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    # разбиваем по основному разделителю
    ings = [ing.strip() for ing in full_text.split(';') if ing.strip()]

    final = []
    for ing in ings:
        ing = ing.strip(' .,;')
        ing = re.sub(r'([a-z])([A-Z])', r'\1 \2', ing)
        ing = re.sub(r'\s+', ' ', ing)
        if len(ing) > 3 and ing.lower() not in ['inci', 'and', 'et', 'und']:
            final.append(ing)

    return final