from unittest.mock import patch
from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"


def test_llm_normal_response():
    pass


def test_llm_gibberish_response():
    pass


@patch('src.translator.get_language', return_value="Spanish")
@patch('src.translator.get_translation', return_value="I don't understand your request")
def test_unexpected_language(mock_translation, mock_language):
    # we mock the model's response to return a random message
    # mocker.return_value.message.content = "I don't understand your request"

    # TODO assert the expected behavior
    result = translate_content("Hier ist dein erstes Beispiel.")
    # print(result)
    assert result == (True, "Hier ist dein erstes Beispiel.")


@patch('src.translator.get_language', return_value=None)
@patch('src.translator.get_translation', return_value=None)
def test_invalid_format_not_tuple(mock_translation, mock_language):
    # Case 2: LLM returns something that's not a tuple
    result = translate_content("Bonjour, comment ça va ?")
    # Should still return the fallback
    assert result == (True, "Bonjour, comment ça va ?")


@patch('src.translator.get_language', return_value=123)
@patch('src.translator.get_translation', return_value=["not a string"])
def test_type_error_in_bool_field(mock_translation, mock_language):
    # Case 3: LLM returns tuple but with wrong types
    result = translate_content("Hola amigo!")
    # Should handle type mismatch safely
    assert result == (True, "Hola amigo!")


@patch('src.translator.get_language', side_effect=Exception("Network error"))
def test_exception_during_query(mock_language):
    # Case 4: The LLM call itself raises an exception
    result = translate_content("Ciao, mi chiamo Luca.")
    # Should catch the exception and recover
    assert result == (True, "Ciao, mi chiamo Luca.")


@patch('src.translator.get_language', return_value="   ")
@patch('src.translator.get_translation', return_value="   ")
def test_empty_model_response(mock_translation, mock_language):
    # Case 5: LLM returns an empty or whitespace-only message
    result = translate_content("Привет, как дела?")
    # Should detect invalid or empty text and fall back safely
    assert result == (True, "Привет, как дела?")


# 5. Test when language detected is non-English and translation is valid
@patch('src.translator.get_language', return_value="fr")
@patch('src.translator.get_translation', return_value="hello")
def test_valid_translation(mock_lang, mock_trans):
    result = translate_content("bonjour")
    assert result == (False, "hello")


# 6. Test when LLM returns English text (should skip translation)
@patch('src.translator.get_language', return_value="en")
@patch('src.translator.get_translation', return_value="")
def test_already_english(mock_lang, mock_trans):
    result = translate_content("good morning")
    assert result == (True, "")