from flask import Flask, request, jsonify, render_template,send_file
import mysql.connector
import google.generativeai as genai
import requests
import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace with your Gemini 1.5 FLASH API Key
GEMINI_API_KEY = "YOUR API KEY"      
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

driver = None
bug_logs = []

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR PASSWORD",
        database="YOUR DATABASE NAME"
    )  

# Store logs in MySQL
def log_request(user_api_url, method, response_time, status_code, response_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (user_api_url, method, response_time, status_code, response_text) 
        VALUES (%s, %s, %s, %s, %s)
    """, (user_api_url, method, response_time, status_code, response_text[:500]))
    conn.commit()
    cursor.close()
    conn.close()

# Generate anomaly report using Gemini 1.5 FLASH SDK
def generate_anomaly_report(api_url, method, status_code, response_time, response_text):
    prompt = f"""
    Analyze the following API response details and identify any anomalies or issues:
    - API URL: {api_url}
    - Method: {method}
    - Status Code: {status_code}
    - Response Time: {response_time:.2f} seconds
    - Response Body (trimmed): {response_text[:500]}

    Provide a short summary of any potential problems, errors, or recommendations.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini SDK error: {str(e)}"

@app.route('/')
def index():
    return render_template('final.html')

@app.route('/bug-detector')
def bug_detector():
    return render_template('index1.html')

@app.route('/anomaly-detector')
def anomaly_detector():
    return render_template('API.html')

@app.route("/start_testing", methods=["POST"])
def start_testing():
    global driver
    data = request.get_json()
    if not data or "website_url" not in data:
        return jsonify({"error": "Missing 'website_url' in request body"}), 400

    website_url = data["website_url"]
    
    if driver:
        return jsonify({"message": "Browser already running!"})

    try:
        driver = uc.Chrome()
        driver.get(website_url)
        time.sleep(2)
        return jsonify({"message": f"Website {website_url} loaded successfully."})
    except Exception as e:
        bug_logs.append(f"Error loading website: {str(e)}")
        return jsonify({"error": "Failed to load website!"}), 500

@app.route("/perform_action", methods=["POST"])
def perform_action():
    global driver
    if not driver:
        return jsonify({"error": "Start testing first!"}), 400

    data = request.get_json()
    if not data or "action" not in data or "selector" not in data:
        return jsonify({"error": "Missing 'action' or 'selector' in request body"}), 400

    action = data["action"].upper()
    selector = data["selector"]
    text = data.get("text", "")

    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        if action == "CLICK":
            element.click()
            return jsonify({"message": f"Clicked on {selector}"})
        elif action == "TYPE":
            element.send_keys(text)
            element.send_keys(Keys.RETURN)
            return jsonify({"message": f"Typed '{text}' into {selector}"})
        elif action == "VERIFY":
            return jsonify({"message": f"Element {selector} found!"})
        elif action == "WAIT":
            time.sleep(2)
            return jsonify({"message": "Waited for 2 seconds."})
        else:
            return jsonify({"error": "Invalid action. Use CLICK, TYPE, VERIFY, or WAIT"}), 400
    except Exception as e:
        bug_logs.append(f"Error performing {action} on {selector}: {str(e)}")
        return jsonify({"error": f"Failed to {action} {selector}"}), 500

@app.route("/generate_report", methods=["GET"])
def generate_report():
    bug_log_text = "\n".join(bug_logs) if bug_logs else "No errors detected."

    debug_prompt = f"""
    Errors encountered:
    {bug_log_text}
    Suggest fixes and best practices.
    """
    
    try:
        response = model.generate_content(debug_prompt)
        analysis = response.text if response else "Gemini AI could not generate a response."
    except Exception as e:
        analysis = "Gemini AI error: " + str(e)

    report_content = f"{bug_log_text}\n\nGemini Analysis:\n{analysis}"

    with open("bug_report.txt", "w") as file:
        file.write(report_content)

    return jsonify({"message": "Bug report generated!", "report": report_content})

@app.route("/stop_testing", methods=["GET"])
def stop_testing():
    global driver
    if driver:
        driver.quit()
        driver = None
        return jsonify({"message": "Testing stopped, browser closed."})
    return jsonify({"message": "No active browser session!"})

@app.route('/fetch_api', methods=['POST'])
def fetch_api():
    data = request.json
    user_api_url = data.get("api_url")
    method = data.get("method", "GET").upper()
    payload = data.get("payload", {})

    if not user_api_url:
        return jsonify({"error": "API URL is required"}), 400

    start_time = time.time()

    try:
        if method == "GET":
            response = requests.get(user_api_url)
        elif method == "POST":
            response = requests.post(user_api_url, json=payload)
        elif method == "PUT":
            response = requests.put(user_api_url, json=payload)
        elif method == "PATCH":
            response = requests.patch(user_api_url, json=payload)
        elif method == "DELETE":
            response = requests.delete(user_api_url)
        else:
            return jsonify({"error": "Invalid HTTP method"}), 400

        status_code = response.status_code
        response_text = response.text
    except requests.exceptions.RequestException as e:
        status_code = 500
        response_text = str(e)

    response_time = time.time() - start_time

    # Log request
    log_request(user_api_url, method, response_time, status_code, response_text)

    # Get anomaly report from Gemini
    gemini_report = generate_anomaly_report(user_api_url, method, status_code, response_time, response_text)

    return jsonify({
        "api_url": user_api_url,
        "method": method,
        "status_code": status_code,
        "response_time": round(response_time, 2),
        "response": response_text[:300],
        "anomaly_report": gemini_report
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
   
