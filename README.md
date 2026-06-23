# Анализ состава косметики с помощью ИИ

**Проект по курсу "Программная инженерия"**

Это приложение позволяет по фото этикетки косметического средства автоматически распознать состав ингредиентов и получить понятное объяснение на русском языке: что это за компонент, для чего используется и насколько безопасен.

## Технологии

- **OCR**: EasyOCR - распознавание текста с фото
- **LLM**: Qwen2.5-7B-Instruct (через Hugging Face API) - анализ, перевод и упрощение текста
- **Backend**: FastAPI
- **Frontend**: Streamlit

## Как запустить локально
1. клонируйте репозиторий:
   ```
   git clone https://github.com/duckkk7/cosmetics-analyzer.git
3. создайте виртуальное окружение
4. установите зависимости:
   ```
   pip install -r requirements.txt
5. создайте файл .env в корне проекта и добавьте свой токен Hugging Face (или настройте переменные среды у себя в иде)
   ```
   HF_TOKEN=ваш_токен
6. запустите backend (или через uvicorn)
   ```
   fastapi dev main.py
7. в отдельном терминале запустите Streamlit:
   ```
   streamlit run app/frontend/app.py

## Скриншоты
**Главный экран**
<img width="1920" height="869" alt="image" src="https://github.com/user-attachments/assets/69a597bc-e879-4914-a3c4-c332a8d6f3dd" />

**Пример анализа**
<img width="1920" height="869" alt="image" src="https://github.com/user-attachments/assets/5ae00fdd-ba7a-44cc-9700-70e83d220385" />
