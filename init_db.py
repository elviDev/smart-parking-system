from app import create_app, db
from app.models import ParkingSlot

def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Check if we have slots
        count = ParkingSlot.query.count()
        if count == 0:
            print("Creating 10 parking slots...")
            for i in range(1, 11):
                slot = ParkingSlot(slot_number=str(i))
                db.session.add(slot)
            db.session.commit()
            print("✅ Created 10 parking slots!")
        else:
            print(f"✅ Found {count} parking slots already.")
        
        print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_database()