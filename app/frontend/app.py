import streamlit as st
import os
import sys

# import requests
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from app.core.ocr import ocr_image
from app.core.llm import ask_llm

API_URL = "https://cosmetics-analyzer.onrender.com"

st.set_page_config(
    page_title="Анализ состава косметики",
    page_icon="🧴",
    layout="wide"
)

st.title("🧴 Анализ состава косметики")
st.markdown("Загрузите фото этикетки — я разберу ингредиенты и объясню их простым языком!")

with st.form(key="upload_form"):
    uploaded_file = st.file_uploader("Загрузите фото состава", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button("Анализировать")

if submit_button and uploaded_file:
    st.image(uploaded_file, caption="Загруженное фото")
    with st.spinner("Анализирую фото..."):
        try:
            # files = {"file": uploaded_file}
            # response = requests.post(f"{API_URL}/api/analyze", files=files, timeout=None)

            #     if response.status_code == 200:
            #         data = response.json()
            #         results = data.get("results", [])
            #
            #         if not results:
            #             st.warning("Ничего не найдено.")
            #         else:
            #             st.success("Готово!")
            #             st.markdown("### Результаты анализа:")
            #             for text in results:
            #                 st.markdown(text)
            #     else:
            #         st.error(f"Ошибка сервера: {response.status_code} — {response.text}")
            #
            # except requests.exceptions.RequestException as e:
            #     st.error(f"Не удалось подключиться: {e}")

            image_bytes = uploaded_file.getvalue()

            ingredients_list = ocr_image(image_bytes)

            if not ingredients_list:
                st.warning("Не удалось распознать текст на изображении. Попробуйте другое фото.")
            else:
                st.info(f"Успешно распознано ингредиентов: {len(ingredients_list)}")

                with st.spinner("Связываюсь с экспертной нейросетью..."):
                    prompt = f"""
                                Ты — эксперт по косметике. Вот состав продукта на английском:

                                {ingredients_list}

                                Твоя задача:
                                1. Разбей на отдельные ингредиенты (если какие-то совершенно разные элементы состава оказались в одной строке — раздели).
                                2. Укажи простым языком: что это, для чего используется, польза/риск для кожи.
                                3. Оцени безопасность (безопасен, применять с осторожностью, нежелательно).
                                4. Ответь в формате нумерованного списка, красиво и понятно на русском языке согласно примеру. ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ. НЕ ИСПОЛЬЗУЙ КИТАЙСКИЙ И ДРУГИЕ ЯЗЫКИ. НЕ ДУБЛИРУЙ ОТВЕТ.
                                (Исходное наименование - описание, функциональность, безопасность).
                                5. Если видишь текст, который по твоему мнению уже не является элементом состава, то игнорируй его.
                                Пример:
                                1. Glycerin  - увлажняет кожу, безопасен для кожи.
                                2. Niacinamide  - укрепляет барьер, борется с акне, безопасен.
                                """

                    explanation = ask_llm(prompt)

                    results = [line.strip() for line in explanation.split("\n") if line.strip()]

                    st.success("Анализ успешно завершен!")
                    st.markdown("### Результаты анализа:")
                    for text in results:
                        st.markdown(text)

        except Exception as e:
            st.error(f"Произошла ошибка при обработке: {e}")
            # if "TesseractNotFoundError" in str(e) and platform.system() == "Windows":
            #     st.info("Подсказка для Windows: проверьте правильность пути к tesseract.exe в файле app/core/ocr.py")

st.markdown("---")
st.info("""
**Важно!**  
Ответы созданы с помощью генеративной языковой модели (LLM) и не являются медицинской консультацией.  
Это **не замена** мнению дерматолога или токсиколога.  
Если у вас ранее были аллергические реакции при использовании средств с похожими компонентами — 
обязательно проконсультируйтесь с врачом!
""")
