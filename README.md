# 🗞️ Notifly - Campus Newsletter System

A modern, responsive campus newsletter system built with Flask and vanilla JavaScript.

## ✨ Features

- **Modern UI**: Glass-morphism design with responsive layout
- **Real-time Validation**: Form validation with instant feedback
- **File Uploads**: Support for images and documents
- **Admin Dashboard**: Review and manage submissions
- **Offline Support**: Local storage backup when server is unavailable
- **Multiple Fallbacks**: Reliable submission with endpoint redundancy

## 🏗️ Architecture

### Frontend
- **HTML5 + CSS3**: Modern semantic markup with glass-morphism styling
- **Vanilla JavaScript**: Form handling, validation, and API communication
- **Responsive Design**: Mobile-first approach with CSS Grid

### Backend
- **Flask**: Python web framework for API endpoints
- **SQLite**: Database for storing submissions
- **CORS**: Cross-origin resource sharing enabled
- **File Handling**: Upload support for attachments

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shashwatjaiswal2025-blip/Notifly_project.git
   cd Notifly_project
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the Flask backend**
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5000`

4. **Start the frontend server**
   ```bash
   # In a new terminal, from project root
   python -m http.server 8000
   ```
   Frontend will be available at `http://localhost:8000`

## 📱 Usage

1. **Main Website**: Visit `http://localhost:8000/index.html`
2. **Submit News**: Use the form at `http://localhost:8000/templates/submit.html`
3. **Admin Dashboard**: View submissions at `http://localhost:8000/admin.html`

## 🗄️ Database Schema

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

## 🛠️ API Endpoints

- `GET /api/test` - Health check
- `POST /api/submit-news` - Submit news article
- `GET /api/submissions` - Retrieve all submissions

## 📁 Project Structure

```
Notifly/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── notifly.db         # SQLite database
│   └── uploads/           # File storage
├── templates/
│   ├── index.html         # Alternative homepage
│   └── submit.html        # Submission form
├── admin.html             # Admin dashboard
├── index.html            # Main homepage
└── test-submit.html      # Testing form
```

## 🔧 Development

### Adding New Features
1. Backend changes go in `backend/app.py`
2. Frontend styling in the `<style>` sections
3. JavaScript functionality in `<script>` sections

### Database Management
- View submissions: Run `python backend/view_submissions.py`
- Direct database access: SQLite browser or command line

## 🌟 Key Components

### Form Validation
- Real-time field validation
- Email format checking
- Required field indicators
- Error state management

### Error Handling
- Multiple endpoint attempts
- Local storage fallback
- User-friendly error messages
- Connection status feedback

### File Uploads
- Drag-and-drop interface
- Multiple file support
- File type restrictions
- Upload progress feedback

## 🎨 Design System

- **Primary Color**: #667eea (Purple Blue)
- **Gradient**: 135deg, #667eea 0%, #764ba2 100%
- **Typography**: Arial, sans-serif
- **Effects**: Glass-morphism with backdrop-filter blur

## 🔐 Security Features

- SQL injection protection with parameterized queries
- Input validation on both frontend and backend
- File type restrictions for uploads
- CORS configuration for controlled access

## 📊 Testing

1. **Form Submission**: Use the test form with debug features
2. **API Testing**: Direct endpoint testing via browser or Postman
3. **Database Verification**: Check submissions via admin dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- **GitHub**: https://github.com/shashwatjaiswal2025-blip/Notifly_project
- **Live Demo**: (Add your deployment URL here)

## 👥 Team

Created by [shashwatjaiswal2025-blip](https://github.com/shashwatjaiswal2025-blip) and collaborators.

---

Made with ❤️ for campus communities