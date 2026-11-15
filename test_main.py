from main import subtract

def test_positive_numbers():
    assert subtract(20, 8) == 12

def test_negative_result():
    assert subtract(5, 10) == -5

def test_zero():
    assert subtract(10, 10) == 0

def test_decimal_numbers():
    assert subtract(5.5, 2.5) == 3.0