from app import db
from models import User

def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

#Czy można zarejestrować nowego użytkownika
def test_register_new_user(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass',
        'password2': 'testpass'
    }, follow_redirects=True)

    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Cadastro realizado com sucesso" in response_text

#Czy nie można zarejestrować istniejącego użytkownika
def test_register_existing_user(client):
    with client.application.app_context():
        create_user('existinguser', 'password123')

    response = client.post('/register', data={
        'username': 'existinguser',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "O usuário com esse login já existe" in response_text

#Czy dostajesz błąd przy różnych hasłach
def test_register_password_mismatch(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password1',
        'password2': 'password2'
    }, follow_redirects=True)

    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "As senhas não são as mesmas" in response_text

#Czy logowanie działa dla poprawnych danych
def test_login_success(client):
    with client.application.app_context():
        create_user('loginuser', 'testpassword')

    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'testpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Login realizado com sucesso" in response_text

#Czy logowanie odrzuca błędne dane
def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Detalhes de login incorretos" in response_text

#Czy nowe login jest dostępny
def test_check_username_available(client):
    response = client.post('/check_username', json={
        'username': 'uniqueuser'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["available"] == True

#Czy zajęty login jest oznaczony jako niedostępny
def test_check_username_unavailable(client):
    with client.application.app_context():
        create_user('takenuser', 'password123')

    response = client.post('/check_username', json={
        'username': 'takenuser'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["available"] == False

#Czy /logout wymaga zalogowania
def test_logout_requires_login(client):
    response = client.get('/logout', follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert "Login" in response_text or "login" in response_text

#Czy /relatório wymaga zalogowania
def test_access_restriction_to_report(client):
    response = client.get('/relatório', follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert "Login" in response_text or "login" in response_text

#Czy zwykły użytkownik nie widzi strony raportu
def test_access_report_non_admin(client):
    with client.application.app_context():
        user = User(username='regularuser', is_admin=False)
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={
        'username': 'regularuser',
        'password': 'testpassword'
    }, follow_redirects=True)

    response = client.get('/relatório', follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert "Produto" in response_text or "produto" in response_text

#Czy admin może normalnie wejść na stronę raportu
def test_access_report_admin(client):
    with client.application.app_context():
        user = User(username='adminuser', is_admin=True)
        user.set_password('adminpass')
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={
        'username': 'adminuser',
        'password': 'adminpass'
    }, follow_redirects=True)
    response = client.get('/relatório', follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert "Relatório" in response_text or "relatório" in response_text
