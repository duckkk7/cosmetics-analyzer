import streamlit as st
import requests

API_URL = "http://localhost:8000/api/analyze"

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
            files = {"file": uploaded_file}
            response = requests.post(API_URL, files=files, timeout=None)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if not results:
                    st.warning("Ничего не найдено.")
                else:
                    st.success("Готово!")
                    st.markdown("### Результаты анализа:")
                    for text in results:
                        st.markdown(text)
            else:
                st.error(f"Ошибка сервера: {response.status_code} — {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Не удалось подключиться: {e}")


st.markdown("---")
st.info("""
**Важно!**  
Ответы созданы с помощью генеративной языковой модели (LLM) и не являются медицинской консультацией.  
Это **не замена** мнению дерматолога или токсиколога.  
Если у вас ранее были аллергические реакции при использовании средств с похожими компонентами — 
обязательно проконсультируйтесь с врачом!
""")
