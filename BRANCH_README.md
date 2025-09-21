# Notifly - Campus Newsletter System

## 🎯 Project Overview
A complete campus newsletter web application with submission forms, admin dashboard, and database management.

## 📁 Project Structure
```
📂 Notifly/
├── 📂 backend/                 # Flask backend server
│   ├── app.py                  # Main Flask application
│   ├── notifly.db             # SQLite database
│   ├── requirements.txt        # Python dependencies
│   └── 📂 uploads/            # File storage
├── 📂 templates/              # HTML templates
│   ├── index.html             # Alternative homepage
│   └── submit.html            # News submission form
├── admin.html                 # Admin dashboard
├── index.html                 # Main website
└── test-submit.html           # Testing form
```

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
**Backend runs on:** http://localhost:5000

### 2. Frontend Setup
```bash
# In main directory
python -m http.server 8000
```
**Frontend runs on:** http://localhost:8000

## 🌐 Access Points
- **Main Website**: http://localhost:8000/index.html
- **Submit Form**: http://localhost:8000/templates/submit.html
- **Admin Dashboard**: http://localhost:8000/admin.html
- **API Endpoints**: http://localhost:5000/api/

## 💾 Database Schema
```sql
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    organization TEXT,
    description TEXT NOT NULL,
    event_date TEXT,
    event_time TEXT,
    location TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    contact_name TEXT,
    submitted_at TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
);
```

## ✨ Features
- ✅ Responsive glass-morphism UI
- ✅ Real-time form validation
- ✅ File upload support
- ✅ Admin dashboard
- ✅ SQLite database
- ✅ CORS-enabled API
- ✅ Local storage fallback
- ✅ Multiple endpoint redundancy

## 🔧 Technical Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask, SQLite
- **UI Design**: Glass-morphism, CSS Grid
- **APIs**: RESTful endpoints with JSON responses

## 📝 API Endpoints
- `GET /api/test` - Health check
- `POST /api/submit-news` - Submit news article
- `GET /api/submissions` - View all submissions

## 🤝 Contributing
This project is part of the campus newsletter initiative. 

## 📄 License
Campus Newsletter System - Educational Use

---
**Branch**: newsletter-system  
**Created**: September 21, 2025  
**Status**: ✅ Fully Functional