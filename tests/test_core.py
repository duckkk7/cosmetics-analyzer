import pytest
from unittest.mock import patch, MagicMock
from app.core.ocr import ocr_image
from app.core.llm import ask_llm


@patch('app.core.ocr.pytesseract.image_to_string')
@patch('app.core.ocr.cv2.imdecode')
def test_ocr_image_success(mock_imdecode, mock_image_to_string):
    """Тестируем, что OCR успешно извлекает строки текста из байт картинки"""
    # симулируем, что OpenCV успешно декодировал картинку
    mock_imdecode.return_value = MagicMock()
    # симулируем, что Tesseract нашел на картинке ингредиенты
    mock_image_to_string.return_value = "Water, Glycerin, Phenoxyethanol"
    fake_bytes = b"fake_image_bytes"
    result = ocr_image(fake_bytes)
    # проверяем, что функция вернула строку с текстом
    assert "Water" in result
    assert "Glycerin" in result
    mock_image_to_string.assert_called_once()


@patch('app.core.llm.requests.post')
def test_ask_llm_success(mock_post):
    """Тестируем, что модуль LLM корректно обрабатывает успешный ответ от Hugging Face API"""
    # настраиваем фейковый ответ от API Hugging Face
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"generated_text": "Результат анализа состава"}]
    mock_post.return_value = mock_response

    result = ask_llm("Тестовый промпт")

    assert result == "Результат анализа состава"
    mock_post.assert_called_once()


@patch('app.core.llm.requests.post')
def test_ask_llm_failure(mock_post):
    """Тестируем поведение системы при ошибке API Hugging Face"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    # проверяем, что код возвращает строку с ошибкой, а не падает
    result = ask_llm("Тестовый промпт")
    assert "Ошибка" in result or "500" in result