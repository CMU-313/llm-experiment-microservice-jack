import pytest
from unittest.mock import patch
from src.translator import translate_content

# =========================
# Evaluation datasets
# =========================
complete_eval_set = [
    # === Non-English Posts (≥15) ===
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": (False, "Here is your first example.")},
    {"post": "Bonjour, comment ça va ?", "expected_answer": (False, "Hello, how are you?")},
    {"post": "Hola amigo!", "expected_answer": (False, "Hello friend!")},
    {"post": "Ciao, mi chiamo Luca.", "expected_answer": (False, "Hi, my name is Luca.")},
    {"post": "おはようございます。", "expected_answer": (False, "Good morning.")},
    {"post": "¿Dónde está la biblioteca?", "expected_answer": (False, "Where is the library?")},
    {"post": "Das Wetter ist heute schön.", "expected_answer": (False, "The weather is nice today.")},
    {"post": "Je voudrais un café, s'il vous plaît.", "expected_answer": (False, "I would like a coffee, please.")},
    {"post": "Grazie mille per il tuo aiuto.", "expected_answer": (False, "Thank you very much for your help.")},
    {"post": "Привет, как дела?", "expected_answer": (False, "Hi, how are you?")},
    {"post": "안녕하세요. 저는 학생입니다.", "expected_answer": (False, "Hello. I am a student.")},
    {"post": "你好，欢迎来到我们的社区。", "expected_answer": (False, "Hello, welcome to our community.")},
    {"post": "Buongiorno, oggi fa molto freddo.", "expected_answer": (False, "Good morning, it is very cold today.")},
    {"post": "¿Puedes ayudarme con mi tarea?", "expected_answer": (False, "Can you help me with my homework?")},
    {"post": "Merci beaucoup pour votre tiempo.", "expected_answer": (False, "Thank you very much for your time.")},
    {"post": "Сегодня прекрасный день для прогулки.", "expected_answer": (False, "Today is a beautiful day for a walk.")},
    {"post": "這是一個測試。", "expected_answer": (False, "This is a test.")},

    # === English Posts (≥15) ===
    {"post": "Thanks for your help today!", "expected_answer": (True, "Thanks for your help today!")},
    {"post": "This project is going great so far.", "expected_answer": (True, "This project is going great so far.")},
    {"post": "Can you send me the report?", "expected_answer": (True, "Can you send me the report?")},
    {"post": "I'm looking forward to the weekend.", "expected_answer": (True, "I'm looking forward to the weekend.")},
    {"post": "We need to meet at 3pm.", "expected_answer": (True, "We need to meet at 3pm.")},
    {"post": "I really appreciate your feedback.", "expected_answer": (True, "I really appreciate your feedback.")},
    {"post": "How was your morning?", "expected_answer": (True, "How was your morning?")},
    {"post": "Could you please clarify that last point?", "expected_answer": (True, "Could you please clarify that last point?")},
    {"post": "Our results exceeded expectations this quarter.", "expected_answer": (True, "Our results exceeded expectations this quarter.")},
    {"post": "I’ll update the document and send it by tomorrow.", "expected_answer": (True, "I’ll update the document and send it by tomorrow.")},
    {"post": "It’s been raining all afternoon.", "expected_answer": (True, "It’s been raining all afternoon.")},
    {"post": "Let’s grab lunch later.", "expected_answer": (True, "Let’s grab lunch later.")},
    {"post": "The system crashed unexpectedly.", "expected_answer": (True, "The system crashed unexpectedly.")},
    {"post": "Everything is working perfectly now.", "expected_answer": (True, "Everything is working perfectly now.")},
    {"post": "Our team did an amazing job on the release.", "expected_answer": (True, "Our team did an amazing job on the release.")},
    {"post": "The concert last night was incredible!", "expected_answer": (True, "The concert last night was incredible!")},

    # === Unintelligible / Malformed Posts (≥5) ===
    {"post": "asdfghjkl", "expected_answer": (True, "asdfghjkl")},
    {"post": "123456789", "expected_answer": (True, "123456789")},
    {"post": "uhh???!!!", "expected_answer": (True, "uhh???!!!")},
    {"post": "🥸🤖🚀", "expected_answer": (True, "🥸🤖🚀")},
    {"post": "lorem ipsum dolor sit amet", "expected_answer": (True, "lorem ipsum dolor sit amet")},
    {"post": "blargh wooo zzz?", "expected_answer": (True, "blargh wooo zzz?")},
]

translation_eval_set = [
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": "Here is your first example."},
    {"post": "Bonjour, comment ça va ?", "expected_answer": "Hello, how are you?"},
    {"post": "Hola amigo!", "expected_answer": "Hello friend!"},
    {"post": "Ciao, mi chiamo Luca.", "expected_answer": "Hi, my name is Luca."},
    {"post": "おはようございます。", "expected_answer": "Good morning."},
    {"post": "¿Dónde está la biblioteca?", "expected_answer": "Where is the library?"},
    {"post": "Je voudrais un café, s'il vous plaît.", "expected_answer": "I would like a coffee, please."},
    {"post": "Das Wetter ist heute schön.", "expected_answer": "The weather is nice today."},
    {"post": "Grazie mille per il tuo aiuto.", "expected_answer": "Thank you very much for your help."},
    {"post": "안녕하세요. 저는 학생입니다.", "expected_answer": "Hello. I am a student."},
    {"post": "你好，欢迎来到我们的社区。", "expected_answer": "Hello, welcome to our community."},
    {"post": "Привет, как дела?", "expected_answer": "Hi, how are you?"},
]

language_detection_eval_set = [
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": "German"},
    {"post": "Bonjour, comment ça va ?", "expected_answer": "French"},
    {"post": "Hola amigo!", "expected_answer": "Spanish"},
    {"post": "Ciao, mi chiamo Luca.", "expected_answer": "Italian"},
    {"post": "おはようございます。", "expected_answer": "Japanese"},
    {"post": "¿Dónde está la biblioteca?", "expected_answer": "Spanish"},
    {"post": "Je voudrais un café, s'il vous plaît.", "expected_answer": "French"},
    {"post": "Das Wetter ist heute schön.", "expected_answer": "German"},
    {"post": "Grazie mille per il tuo aiuto.", "expected_answer": "Italian"},
    {"post": "안녕하세요. 저는 학생입니다.", "expected_answer": "Korean"},
    {"post": "你好，欢迎来到我们的社区。", "expected_answer": "Chinese"},
    {"post": "Привет, как дела?", "expected_answer": "Russian"},
]

# =========================
# Happy-path tests (parameterized)
# =========================

@pytest.mark.parametrize("case", translation_eval_set)
@patch('src.translator.get_language', return_value="xx")  # any non-EN marker
def test_llm_normal_response(mock_lang, case):
    """
    Non-English posts should be translated. is_english=False, content=expected translation.
    """
    with patch('src.translator.get_translation', return_value=case["expected_answer"]):
        assert translate_content(case["post"]) == (False, case["expected_answer"])


english_cases = [c for c in complete_eval_set if c["expected_answer"][0] is True]

@pytest.mark.parametrize("case", english_cases)
@patch('src.translator.get_language', return_value="en")
@patch('src.translator.get_translation', return_value="")  # shouldn’t be called
def test_english_passthrough_from_eval_set(mock_trans, mock_lang, case):
    """
    English posts should pass through unchanged. is_english=True, content=original post.
    """
    assert translate_content(case["post"]) == (True, case["post"])


# =========================
# Gibberish passthrough (parameterized)
# =========================

gibberish_posts = {"asdfghjkl", "123456789", "uhh???!!!", "🥸🤖🚀", "blargh wooo zzz?"}
gibberish_cases = [c for c in complete_eval_set if c["post"] in gibberish_posts]

@pytest.mark.parametrize("case", gibberish_cases)
@patch('src.translator.get_language', return_value="I don't understand your request")
@patch('src.translator.get_translation', return_value="")
def test_llm_gibberish_response(mock_trans, mock_lang, case):
    """
    If the model 'doesn't understand' and returns no translation, passthrough the original.
    """
    assert translate_content(case["post"]) == (True, case["post"])


# =========================
# Edge / robustness tests (kept separate)
# =========================

@patch('src.translator.get_language', return_value="Spanish")
@patch('src.translator.get_translation', return_value="I don't understand your request")
def test_unexpected_language(mock_trans, mock_lang):
    """
    Model says 'Spanish' for a German sentence and fails to translate: fallback to passthrough.
    """
    result = translate_content("Hier ist dein erstes Beispiel.")
    assert result == (True, "Hier ist dein erstes Beispiel.")


@patch('src.translator.get_language', return_value=None)
@patch('src.translator.get_translation', return_value=None)
def test_invalid_format_not_tuple(mock_trans, mock_lang):
    """
    None responses from both detectors: treat as unknown and passthrough.
    """
    result = translate_content("Bonjour, comment ça va ?")
    assert result == (True, "Bonjour, comment ça va ?")


@patch('src.translator.get_language', return_value=123)
@patch('src.translator.get_translation', return_value=["not a string"])
def test_type_error_in_bool_field(mock_trans, mock_lang):
    """
    Bad types returned from helpers: ensure function handles and falls back safely.
    """
    result = translate_content("Hola amigo!")
    assert result == (True, "Hola amigo!")


@patch('src.translator.get_language', side_effect=Exception("Network error"))
def test_exception_during_query(mock_lang):
    """
    Exceptions in language detection should not crash the function: fallback to passthrough.
    """
    result = translate_content("Ciao, mi chiamo Luca.")
    assert result == (True, "Ciao, mi chiamo Luca.")


@patch('src.translator.get_language', return_value="   ")
@patch('src.translator.get_translation', return_value="   ")
def test_empty_model_response(mock_trans, mock_lang):
    """
    Empty/whitespace responses from helpers: fallback to passthrough.
    """
    result = translate_content("Привет, как дела?")
    assert result == (True, "Привет, как дела?")

