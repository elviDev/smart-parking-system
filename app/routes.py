from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import ParkingSlot, ParkingHistory
from app import db
import cv2
import base64
from datetime import datetime
import numpy as np
import random

bp = Blueprint('main', __name__)

def get_mock_frame():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    for i in range(10):
        x = 50 + i * 55
        y = 200
        color = (0, 255, 0) if i % 2 == 0 else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + 40, y + 80), color, 2)
        cv2.putText(frame, f"Slot {i+1}", (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    cv2.putText(frame, "Smart Parking System", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return frame

@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/test')
def test():
    return "<h1>✅ Flask is working!</h1>"

@bp.route('/api/status')
@login_required
def get_status():
    slots = ParkingSlot.query.all()
    total_slots = len(slots)
    occupied_slots = sum(1 for slot in slots if slot.is_occupied)
    
    return jsonify({
        'total_slots': total_slots,
        'occupied_slots': occupied_slots,
        'available_slots': total_slots - occupied_slots,
        'slots': [{'id': s.id, 'number': s.slot_number, 'occupied': s.is_occupied} 
                 for s in slots]
    })

@bp.route('/api/detect')
@login_required
def detect_parking():
    frame = get_mock_frame()
    
    slots = ParkingSlot.query.all()
    for slot in slots:
        slot.is_occupied = random.choice([True, False])
        slot.last_updated = datetime.utcnow()
    
    db.session.commit()
    
    total_slots = len(slots)
    occupied = sum(1 for s in slots if s.is_occupied)
    history = ParkingHistory(
        total_slots=total_slots,
        occupied_slots=occupied,
        available_slots=total_slots - occupied
    )
    db.session.add(history)
    db.session.commit()
    
    _, buffer = cv2.imencode('.jpg', frame)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        'image': image_base64,
        'timestamp': datetime.utcnow().isoformat(),
        'total_slots': total_slots,
        'occupied_slots': occupied,
        'available_slots': total_slots - occupied,
        'slots': [{'id': s.id, 'number': s.slot_number, 'occupied': s.is_occupied} for s in slots]
    })

@bp.route('/api/history')
@login_required
def get_history():
    history = ParkingHistory.query.order_by(
        ParkingHistory.date.desc()
    ).limit(50).all()
    
    return jsonify([{
        'date': h.date.isoformat(),
        'total_slots': h.total_slots,
        'occupied_slots': h.occupied_slots,
        'available_slots': h.available_slots
    } for h in history])