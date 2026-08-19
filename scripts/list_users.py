import sys, os
sys.path.insert(0, os.getcwd())

from app import create_app
from app import db
from app.models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    if not users:
        print('No users found')
    for u in users:
        print('username:', u.username)
        print('email:   ', u.email)
        print('is_admin:', u.is_admin)
        print('pw hash:', u.password_hash)
        print('---')
