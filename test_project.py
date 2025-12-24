import pytest

from project import luhn, visa, mastercard, amex, maestro, jcb

def test_luhn():
    assert luhn("4539-1488-0343-6467") == True

def test_luhn_2():
    assert luhn("1234-567") == False

def test_visa():
    assert visa("4111-1111-1111-1111") == True

def test_visa_2():
    assert visa("5555-5555-5555-4444") == None

def test_mastercard():
    assert mastercard("5555-5555-5555-4444") == True

def test_mastercard_2():
    assert mastercard("3782-822463-10005") == None

def test_amex():
    assert amex("3782-822463-10005") == True

def test_amex_2():
    assert amex("6762-1234-5678-9012-31") == None

def test_maestro():
    assert maestro("6762-1234-5678-9012-31") == True

def test_maestro_2():
    assert maestro("3530-1113-3330-0000") == None

def test_jcb():
    assert jcb("3530-1113-3330-0000") == True

def test_jcb_2():
    assert jcb("4539-1488-0343-6467") == None
