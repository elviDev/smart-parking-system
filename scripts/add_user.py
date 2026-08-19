import sys, os
sys.path.insert(0, os.getcwd())

from app import create_app, db
from app.models import User

import getpass

USERNAME = os.environ.get('ADD_USER_USERNAME', 'elvis')
EMAIL = os.environ.get('ADD_USER_EMAIL', f'{USERNAME}@example.com')

def main():
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=USERNAME).first()
        if user:
            print('User already exists:', user.username)
            return
        # Password: either from env ADD_USER_PASSWORD or prompt securely
        password = os.environ.get('ADD_USER_PASSWORD')
        if not password:
            password = getpass.getpass(f'Password for new user {USERNAME}: ')
        user = User(username=USERNAME, email=EMAIL)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print('Created user:', USERNAME)

if __name__ == '__main__':
    main()
