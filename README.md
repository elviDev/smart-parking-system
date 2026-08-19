# 🚗 Smart Parking Management System

A compact, easy-to-run Smart Parking Management web app built with Flask and OpenCV.

This project demonstrates a simple pipeline for detecting parking slot occupancy from a camera feed (or demo frames), storing occupancy history, and presenting a responsive dashboard with live feed and trends.

## 📸 Screenshots

![Dashboard](screenshot.png)

## ✨ Features

- 📷 Real-time camera feed with OpenCV
- 🅿️ Automatic parking slot detection
- 📊 Occupancy history visualization
- 🔄 Auto-refresh updates
- 📱 Fully responsive design

## 🛠️ Tech Stack

| Technology          | Purpose            |
| ------------------- | ------------------ |
| Python 3.12         | Backend language   |
| Flask 2.3.2         | Web framework      |
| SQLite / SQLAlchemy | Database           |
| OpenCV 5.0          | Computer vision    |
| Bootstrap 5         | Frontend design    |
| Chart.js            | Data visualization |

## 🚀 Quick Start

````bash
# Clone the repository
git clone https://github.com/elviDev/smart-parking-system.git
cd smart-parking-system

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt

1. Copy `.env.example` to `.env` and set `SECRET_KEY` (do NOT commit `.env`).

2. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
````

3. Initialize the database (this creates the `instance/parking.db` file and sample slots):

```bash
python init_db.py
```

4. (Optional) Create an admin user:

```bash
python create_admin.py
```

5. Run the app:

```bash
python run.py
```

6. Open the UI at `http://127.0.0.1:5000/`.

Security notes:

- The `instance/` folder and `.env` are ignored by `.gitignore` to avoid committing the SQLite DB or secrets.
- Set a strong `SECRET_KEY` in your `.env` for production deployments.
