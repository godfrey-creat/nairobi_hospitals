#! /usr/bin/env python
from api.v1.app import app
from models.models import db

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
