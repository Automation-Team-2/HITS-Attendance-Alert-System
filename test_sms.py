import os
import sys
import json
import time
import random
from datetime import datetime
import requests

# Define paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(BASE_DIR, "test-student.json")
LOG_FILE = os.path.join(BASE_DIR, "sms_log.txt")


def log_sms_status(student_name: str, mobile: str, status: str, details: str):
    """
    Logs the SMS status to sms_log.txt with a timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Student: {student_name} | Mobile: {mobile} | Status: {status} | Details: {details}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)


def send_fast2sms(api_key: str, mobile: str, message: str, is_mock: bool = False) -> dict:
    """
    Sends an SMS using Fast2SMS Dev API (Quick SMS route).
    """
    # If in mock mode, simulate API responses (ideal for testing without API keys/credits)
    if is_mock:
        time.sleep(0.5) # Simulate API response delay
        # 30% chance to fail to demonstrate retry logic
        if random.random() < 0.3:
            return {
                "success": False,
                "details": None,
                "error": "Mock API Call Failed (Simulated rate limit/network error)"
            }
        else:
            return {
                "success": True,
                "details": {"return": True, "request_id": f"mock-req-{random.randint(100000, 999999)}"},
                "error": None
            }

    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "numbers": mobile
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        response_data = response.json()
        
        if response_data.get("return") is True:
            return {
                "success": True,
                "details": response_data,
                "error": None
            }
        else:
            error_message = response_data.get("message", "Unknown Fast2SMS API error")
            return {
                "success": False,
                "details": response_data,
                "error": error_message
            }
            
    except requests.exceptions.HTTPError as http_err:
        try:
            api_error = response.json().get("message")
        except Exception:
            api_error = None
        
        error_details = api_error if api_error else f"HTTP error: {http_err}"
        return {
            "success": False,
            "details": None,
            "error": error_details
        }
    except requests.exceptions.RequestException as err:
        return {
            "success": False,
            "details": None,
            "error": f"Network error: {err}"
        }


def send_sms(provider: str, api_key: str, mobile: str, message: str, is_mock: bool = False) -> dict:
    """
    Unified wrapper function to send SMS notifications.
    Swapping providers in the future will not require modifying main logic.
    """
    provider_lower = provider.strip().lower()
    
    if provider_lower == "fast2sms":
        return send_fast2sms(api_key, mobile, message, is_mock)
    elif provider_lower == "textlocal":
        return {"success": False, "details": None, "error": "Textlocal not implemented yet."}
    elif provider_lower == "msg91":
        return {"success": False, "details": None, "error": "MSG91 not implemented yet."}
    else:
        return {"success": False, "details": None, "error": f"Unsupported provider: {provider}"}


def main():
    api_key ="nYiku3IwOXLnY9BN9NmKEbdanvVPVbSL6koIJqnYQlrjZSBBq9qhZyvzBFRC" # here i used an api key but for regular sms we need to complete one transaction of 100 INR or more before using API route.
    is_mock = False
    print("API KEY FOUND:", api_key)
    print("MOCK MODE:", is_mock)
    is_mock = False
     

    if not api_key:   
        print("Running in MOCK mode to demonstrate JSON reading and etc.")
        print("To send real SMS, set your API key in the terminal first:")
        print(" On Windows (CMD):set FAST2SMS_API_KEY=your_api_key_here")
        print(" On macOS/Linux: export FAST2SMS_API_KEY=\"your_api_key_here\"\n")
        is_mock = True
        api_key = "MOCK_KEY"
        
    if not os.path.exists(STUDENTS_FILE):
        print(f"[ERROR] Student data file not found at: {STUDENTS_FILE}")
        sys.exit(1)
        
    try:
        with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
            students = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse student data JSON: {e}")
        sys.exit(1)
        
    print(f"--- Starting Attendance Alert System ---")
    print(f"Loaded {len(students)} students.")
    print(f"Logging messages to: {LOG_FILE}\n")

    for index, student in enumerate(students):
        name = student.get("name")
        roll_no = student.get("rollNo")
        attendance = student.get("attendance")
        mobile = student.get("mobile")
        
        if not all([name, roll_no, attendance, mobile]):
            continue

        message = (
            f"Attendance Alert: Dear Parent, {name} (Roll No: {roll_no}) has recorded "
            f"an attendance of {attendance}. Please ensure regular attendance."
        )
        
        print(f"[{index + 1}/{len(students)}] Sending alert to {name} ({mobile})...")
        
        response = send_sms("fast2sms", api_key, mobile, message, is_mock)
        
        if response["success"]:
            success_msg = f"SMS accepted. Req ID: {response['details'].get('request_id')}"
            print(f"  -> SUCCESS: {success_msg}")
            log_sms_status(name, mobile, "SUCCESS", success_msg)
        else:
            error_details = response["error"]
            print(f"  -> FAILED: {error_details}")
            print(f"     Retrying in 5 seconds...")
            log_sms_status(name, mobile, "RETRYING", f"First attempt failed: {error_details}")
            
            time.sleep(5)
            
            retry_response = send_sms("fast2sms", api_key, mobile, message, is_mock)
            if retry_response["success"]:
                success_msg = f"SMS accepted on retry. Req ID: {retry_response['details'].get('request_id')}"
                print(f"  -> RETRY SUCCESS: {success_msg}")
                log_sms_status(name, mobile, "SUCCESS_AFTER_RETRY", success_msg)
            else:
                retry_error = retry_response["error"]
                print(f"  -> PERMANENT FAILURE: {retry_error}")
                log_sms_status(name, mobile, "PERMANENT_FAILURE", f"Retry failed: {retry_error}")
        
        if index < len(students) - 1:
            print("Waiting 3 seconds before next message...\n")
            time.sleep(3)

    print("\n--- SMS Alert Process Finished ---")


if __name__ == "__main__":
    main()
