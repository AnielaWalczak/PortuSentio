from app import db, MyProduct, MyComment, User
from flask import json
from datetime import datetime, timedelta


#Sprawdza, czy strona główna (/) ładuje się poprawnie i zawiera nazwę istniejącego produktu.
def test_index_get(client):
    with client.application.app_context():
        product = MyProduct(product_name="Produto Teste", admin_name="admin", active=True)
        db.session.add(product)
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Produto Teste" in response_text

#Sprawdza, czy endpoint /predict zwraca błąd (400) przy pustym komentarzu i 
#odpowiedni komunikat błędu ("Comentário não pode estar vazio").
def test_predict_empty(client):
    response = client.post('/predict', json={"content": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Comentário não pode estar vazio"

#Sprawdza, czy endpoint /predict działa poprawnie, 
# gdy podamy niepusty komentarz – czy zwraca odpowiedź JSON zawierającą klucz "sentiment".
def test_predict_valid(client):
    response = client.post('/predict', json={"content": "Bom produto"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "sentiment" in data

#Sprawdza, czy endpoint /valuate zwraca błąd (400), jeśli komentarz jest pusty
def test_valuate_empty(client):
    response = client.post('/valuate', json={"content": "", "product_id": 1})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Comentário não pode estar vazio"

#Sprawdza, czy endpoint /valuate zwraca błąd (400), gdy nie podano ID produktu.
def test_valuate_no_product_id(client):
    response = client.post('/valuate', json={"content": "Ótimo!", "product_id": None})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Produto não selecionado"

#Sprawdza, czy endpoint /valuate zwraca poprawną wartość "value" dla poprawnego komentarza i istniejącego produktu.
def test_valuate_valid(client):
    response = client.post('/valuate', json={"content": "Muito bom!", "product_id": 1})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "value" in data

#Dodaje unikalny komentarz do bazy i sprawdza, 
# czy endpoint /check-comments prawidłowo liczy liczbę komentarzy dla wybranego produktu w zadanym przedziale czasu.
def test_check_comments(client):
    with client.application.app_context():
        # Utwórz testowego użytkownika-admina i produkt
        admin = User(username="admin_check", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

        product = MyProduct(product_name="Produto Teste", admin_name=admin.username, active=True)
        db.session.add(product)
        db.session.commit()

        unique_content = "Comentário de teste único 12345"
        comment = MyComment(
            product_id=product.product_id,
            user="test_user_check",
            content=unique_content,
            result="positivo",
            value=5,
            created_on=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()

        today = datetime.utcnow()
        today_str = today.strftime('%Y-%m-%d')
        tomorrow_str = (today + timedelta(days=1)).strftime('%Y-%m-%d')
        response = client.get(f'/check-comments?product={product.product_id}&from={today_str}&to={tomorrow_str}')
        assert response.status_code == 200
        data = response.get_json()
        assert "count" in data
        assert data["count"] >= 1

#Sprawdza, czy strona /sucesso (strona sukcesu po dodaniu komentarza) ładuje się poprawnie (status 200).
def test_success_page(client):
    response = client.get('/sucesso')
    assert response.status_code == 200
