from user_crud_api.api import app, db

with app.app_context():
    db.create_all()