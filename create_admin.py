from app import create_app, db
from app.models import User

def create_admin():
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@smartpark.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("✅ Admin user already exists")

if __name__ == '__main__':
    create_admin()