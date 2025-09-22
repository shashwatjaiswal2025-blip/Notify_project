from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Sample newsletter data with improved structure
newsletter_data = [
    (5, "🚨 Emergency Campus Alert", "Campus-wide maintenance scheduled for this weekend. All online services may be temporarily unavailable. Students advised to download materials in advance.", ["#Emergency", "#Maintenance", "#Important"]),
    (4, "🎓 Innovation Challenge Winners", "Congratulations to the Innovation Challenge 2025 winners! Three teams have been selected to receive $50,000 in scholarships and grants for their sustainable technology solutions.", ["#Innovation", "#Scholarship", "#Achievement"]),
    (3, "📚 New Library Extension", "The highly anticipated library extension featuring modern study spaces and digital media center is now open to all students with 24/7 access areas.", ["#Library", "#StudySpaces", "#Campus"]),
    (2, "💼 Career Fair Registration", "Fall Career Fair registration is now open for October 15th. Over 100 companies participating with internships and full-time positions.", ["#CareerFair", "#Jobs", "#Opportunities"]),
    (1, "🔬 Research Symposium", "Graduate and undergraduate students invited to submit abstracts for Annual Research Symposium. Deadline October 1st, winners receive research grants.", ["#Research", "#Symposium", "#Grants"]),
    (4, "🌱 Sustainability Initiative", "New campus-wide sustainability program launched. Solar panels installation completed, reducing energy consumption by 40%.", ["#Sustainability", "#Green", "#Campus"]),
    (3, "📱 Wi-Fi Upgrade Complete", "Campus Wi-Fi infrastructure upgrade completed, providing faster speeds and better coverage across all buildings.", ["#Technology", "#WiFi", "#Upgrade"])
]

def get_priority_color(priority):
    """Return color scheme based on priority level"""
    colors = {
        5: {"bg": "#fee2e2", "border": "#dc2626", "text": "#991b1b"},  # Red - Critical
        4: {"bg": "#fef3c7", "border": "#f59e0b", "text": "#92400e"},  # Orange - High
        3: {"bg": "#dbeafe", "border": "#3b82f6", "text": "#1e40af"},  # Blue - Medium
        2: {"bg": "#d1fae5", "border": "#10b981", "text": "#065f46"},  # Green - Low
        1: {"bg": "#f3f4f6", "border": "#6b7280", "text": "#374151"}   # Gray - Info
    }
    return colors.get(priority, colors[1])

def get_priority_label(priority):
    """Return human-readable priority label"""
    labels = {
        5: "CRITICAL",
        4: "HIGH", 
        3: "MEDIUM",
        2: "LOW",
        1: "INFO"
    }
    return labels.get(priority, "INFO")

@app.route("/")
def home():
    """Main route for campus newsletter"""
    return render_template("index.html")

@app.route("/api/newsletter")
def api_newsletter():
    """API endpoint for frontend integration"""
    # Sort data by priority (highest first)
    sorted_data = sorted(newsletter_data, key=lambda x: x[0], reverse=True)
    
    articles = []
    for item in sorted_data:
        priority, title, summary, tags = item
        
        # Ensure tags is always a list
        if isinstance(tags, str):
            tags = [tags]
        
        article = {
            "subject": title,
            "summary": summary,
            "priority": get_priority_label(priority).lower(),
            "priority_level": priority,
            "tags": tags,
            "date": datetime.now().strftime("%B %d, %Y"),
            "source": "AI Newsletter System"
        }
        articles.append(article)
    
    return jsonify({"articles": articles, "status": "success"})

if __name__ == "__main__":
    print("🚀 Starting Campus Newsletter Server...")
    print("📰 Campus newsletter available at: http://localhost:8080")
    print("🔌 API endpoint available at: http://localhost:8080/api/newsletter")
    app.run(debug=True, port=8080)