# Automated Bug Detection & AI-Powered API Testing Platform

A Flask-based platform integrating automated website testing, bug tracking, anomaly detection, and Gemini 1.5 Flash AI analysis with MySQL logging.


## 🔥 Features
- ✅ **Automated Website Testing** with Selenium & Undetected ChromeDriver
- 🐛 **AI-Powered Bug Analysis** using Gemini 1.5 Flash API
- 📊 **API Response Validation** with Anomaly Detection
- 📦 **MySQL Database Integration** for test logs storage
- 📈 **Interactive Dashboard** with HTML templates
- ⚡ **Real-time Testing Results** visualization

---
![Selenium Bug Detection](Selenium_BugDetection.png)
![API Anomaly Detection](API_AnomalyDetection.png)

## 🛠️ Installation
Clone repository
git clone https://github.com/radhaswaman/Automated-Bug-Detection.git
cd Automated-Bug-Detection

Install dependencies
pip install -r requirements.txt



---

## ⚙️ Configuration

### Google Gemini API Setup
1. Get API key from [Google AI Studio](https://makersuite.google.com/app)
2. Create `.env` file (optional):
GEMINI_API_KEY=your_api_key_here

```
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
```
```
### Configure Database Connection (app.py)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_db_password'
app.config['MYSQL_DB'] = 'testing_platform'

```
---

## 🚀 Usage
Start Flask application
python app.py


Access the platform at `http://localhost:5000`

---

```
project-root/
├── templates/
│ ├── final.html #Results dashboard
│ ├── index1.html #Main testing interface
│ └── API.html #API testing interface
├── app.py #Main application
├── requirements.txt #Dependency list
└── .env  #Environment variables (optional)
```

---
**Project By:**
- Prof. Ranjeetsingh Suryawanshi (Guide)  
- Radha Waman  
- Shreya Wanwe  
- Dhanashri Wankhede  
- Sai Watile
