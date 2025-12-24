from fastapi import APIRouter, UploadFile, File
from app.core.ocr import ocr_image
from app.core.cosing import find_ingredient, load_cosing
from app.core.llm import ask_llm

router = APIRouter()
# cosing_df = load_cosing()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    texts = ocr_image(image_bytes)
    prompt = f"""
    Ты — эксперт по косметике. Вот состав продукта на английском:

    {texts}

    Твоя задача:
    1. Разбей на отдельные ингредиенты (если какие-то совершенно разные элементы соатава оказались в одной строке — раздели).
    2. Укажи простым языком: что это, для чего используется, польза/риск для кожи.
    3. Оцени безопасность (безопасен, применять с осторожностью, нежелательно).
    4. Ответь в формате нумерованного списка, красиво и понятно на русском языке согласно примеру. 
    (Исходное наименование - описание, функциональность, безопасность).
    5. Если видишь текст, который по твоему мнению уже не является элементом состава, то игнорируй его.
    Пример:
    1. Glycerin  - увлажняет кожу, безопасен для кожи.
    2. Niacinamide  - укрепляет барьер, борется с акне, безопасен.
    """
    print('Отправляю промпт в LLM...')
    explanation = ask_llm(prompt)
    print('Получен ответ.')

    lines = [line.strip() for line in explanation.split("\n") if line.strip()]
    return {"results": lines}

