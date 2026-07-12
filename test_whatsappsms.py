import os
import json
import time
from datetime import datetime
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STUDENTS_FILE = os.path.join(BASE_DIR, "test-student.json")
LOG_FILE = os.path.join(BASE_DIR, "whatsapp_log.txt")

API_KEY = os.getenv("write api key when you get access to api okhie!!")

PHONE_NUMBER_ID = "PHONE_NUMBER_ID"
TEMPLATE_NAME = "attendancealert: 75"

MOCK_MODE = True


def log_status(student, mobile, status, details):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"[{datetime.now()}] "
            f"{student} | {mobile} | {status} | {details}\n"
        )

# sending via whatsapp

def send_whatsapp(api_key,
                  phone_number_id,
                  template_name,
                  mobile,
                  variables,
                  mock=False):

    if mock:

        print(f"Mock WhatsApp sent to {mobile}")

        return {
            "success": True,
            "details": {
                "request_id": "MOCK_WHATSAPP"
            }
        }

    url = "https://www.fast2sms.com/dev/whatsapp"

    headers = {
        "Authorization": api_key
    }

    payload = {
        "phone_number_id": phone_number_id,
        "template_name": template_name,
        "numbers": mobile,
        "variables_values": variables
    }

    try:

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if data.get("return"):

            return {
                "success": True,
                "details": data
            }

        return {
            "success": False,
            "details": data
        }

    except Exception as e:

        return {
            "success": False,
            "details": str(e)
        }

# main program

def main():

    if not os.path.exists(STUDENTS_FILE):

        print("Student JSON file not found.")
        return

    with open(STUDENTS_FILE, "r", encoding="utf-8") as file:

        students = json.load(file)

    print(f"\nLoaded {len(students)} students.\n")

    for student in students:

        name = student["name"]
        roll = student["rollNo"]
        attendance = student["attendance"]
        mobile = student["mobile"]

        print(f"Sending WhatsApp to {name}")

        variables = f"{name}|{roll}|{attendance}"

        result = send_whatsapp(
            API_KEY,
            PHONE_NUMBER_ID,
            TEMPLATE_NAME,
            mobile,
            variables,
            MOCK_MODE
        )

        if result["success"]:

            print("SUCCESS\n")

            log_status(
                name,
                mobile,
                "SUCCESS",
                result["details"]
            )

        else:

            print("FAILED\n")

            log_status(
                name,
                mobile,
                "FAILED",
                result["details"]
            )

        time.sleep(2)

    print("Finished.")

if __name__ == "__main__":
    main()