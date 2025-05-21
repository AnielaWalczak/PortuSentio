from app import db
from models import User, MyComment, MyProduct

def test_user_password(client):
    with client.application.app_context():
        user = User(username="testuser2")
        user.set_password("mypassword")
        db.session.add(user)
        db.session.commit()

        loaded_user = User.query.filter_by(username="testuser2").first()
        assert loaded_user is not None
        assert loaded_user.check_password("mypassword")
        assert not loaded_user.check_password("wrongpassword")


def test_create_comment(client):
    with client.application.app_context():
        # Tworzymy produkt najpierw
        product = MyProduct(product_name="Test Product", admin_name="admin", active=True)
        db.session.add(product)
        db.session.commit()

        comment = MyComment(
            product_id=product.product_id, 
            user="tester",
            content="Ótimo produto!",
            result="Positivo",
            value=2
        )
        db.session.add(comment)
        db.session.commit()

        loaded_comment = MyComment.query.first()
        assert loaded_comment is not None
        assert loaded_comment.product.product_name == "Test Product"
        assert loaded_comment.value == 2
        assert loaded_comment.result == "Positivo"


def test_create_product_with_admin(client):
    with client.application.app_context():
        admin_user = User(username="adminuser2", is_admin=True)
        admin_user.set_password("adminpass123!")
        db.session.add(admin_user)
        db.session.commit()

        product = MyProduct(
            product_name="Special Test Product",
            admin_name=admin_user.username,
            active=True
        )
        db.session.add(product)
        db.session.commit()

        loaded_product = MyProduct.query.filter_by(product_name="Special Test Product").first()
        assert loaded_product is not None
        assert loaded_product.product_name == "Special Test Product"
        assert loaded_product.admin_name == "adminuser2"
        assert loaded_product.active is True
