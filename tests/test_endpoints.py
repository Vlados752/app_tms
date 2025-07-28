import requests


def test_homepage_accessible():
    response = requests.get('http://localhost:5001/')
    assert response.status_code == 200
    assert 'Калькулятор' in response.text  # Или любой ожидаемый текст


def test_addition():
    response = requests.post(
        'http://localhost:5001/',
        data={'a': '2', 'b': '3', 'op': 'add'}
    )
    assert response.status_code == 200
    assert '5' in response.text
