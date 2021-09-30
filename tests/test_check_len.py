def test_check_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"Lenth of phrase >= 15 symbols"
