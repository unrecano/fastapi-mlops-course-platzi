from app.predicts.utils import tokenize_text, remove_stopwords, pos_tagging


def test_tokenize_text():
    text = "This is a simple test."
    tokens = tokenize_text(text)
    assert tokens == ["this", "is", "a", "simple", "test", "."]


def test_remove_stopwords():
    tokens = ["this", "is", "a", "simple", "test"]
    # "this", "is", "a" are stopwords
    filtered_tokens = remove_stopwords(tokens)
    assert "this" not in filtered_tokens
    assert "is" not in filtered_tokens
    assert "a" not in filtered_tokens
    assert "simple" in filtered_tokens
    assert "test" in filtered_tokens


def test_pos_tagging():
    # Example tokens that contain nouns
    tokens = ["simple", "test", "dog"]
    tagged_nouns = pos_tagging(tokens)
    # Both test and dog might be interpreted as nouns
    assert isinstance(tagged_nouns, str)
    assert "test" in tagged_nouns or "dog" in tagged_nouns
