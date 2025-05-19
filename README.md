# Automated Bug Detection & AI-Powered API Testing Platform

A Flask-based platform integrating automated website testing, bug tracking, anomaly detection, and Gemini 1.5 Flash AI analysis with MySQL logging.

![Project Banner](https://via.placeholder.com/800x200?text=AI+Powered+Testing+Platform)

## 🔥 Features
- ✅ **Automated Website Testing** with Selenium & Undetected ChromeDriver
- 🐛 **AI-Powered Bug Analysis** using Gemini 1.5 Flash API
- 📊 **API Response Validation** with Anomaly Detection
- 📦 **MySQL Database Integration** for test logs storage
- 📈 **Interactive Dashboard** with HTML templates
- ⚡ **Real-time Testing Results** visualization

---

## 🛠️ Installation
Clone repository
git clone https://github.com/radhaswaman/Automated-Bug-Detection.git
cd Automated-Bug-Detection

Install dependencies
pip install -r requirements.txt

text

---

## ⚙️ Configuration

### Google Gemini API Setup
1. Get API key from [Google AI Studio](https://makersuite.google.com/app)
2. Create `.env` file (optional):
GEMINI_API_KEY=your_api_key_here

text

### MySQL Database Setup
CREATE DATABASE testing_platform;
USE testing_platform;

CREATE TABLE logs (
id INT AUTO_INCREMENT PRIMARY KEY,
user_api_url TEXT,
method VARCHAR(10),
response_time FLOAT,
status_code INT,
response_text TEXT
);

text

### Configure Database Connection (app.py)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_db_password'
app.config['MYSQL_DB'] = 'testing_platform'

text

---

## 🚀 Usage
Start Flask application
python app.py

text
Access the platform at `http://localhost:5000`

---

## 📂 Project Structure
project-root/
├── templates/
│ ├── final.html # Results dashboard
│ ├── index1.html # Main testing interface
│ └── API.html # API testing interface
├── app.py # Main application
├── requirements.txt # Dependency list
└── .env # Environment variables (optional)

text

---

## 📦 Dependencies
- Flask 2.0+
- Selenium 4.0+
- undetected-chromedriver
- google-generativeai
- python-dotenv
- mysql-connector-python

---
