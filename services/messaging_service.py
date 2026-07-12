import os
import httpx
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY", "")

WHATSAPP_PROVIDER = os.getenv("WHATSAPP_PROVIDER", "callmebot")

async def send_whatsapp_callmebot(phone: str, message: str) -> bool:
    if not CALLMEBOT_API_KEY:
        return False
    url = f"https://api.callmebot.com/whatsapp.php"
    params = {"phone": phone, "text": message, "apikey": CALLMEBOT_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=15)
            return resp.status_code == 200
    except Exception:
        return False

async def send_whatsapp_cloud_api(phone: str, message: str) -> bool:
    if not WHATSAPP_API_KEY or not WHATSAPP_PHONE_ID:
        return False
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=15)
            return resp.status_code == 200
    except Exception:
        return False

async def send_alert(phone: str, message: str, channel: str = "whatsapp") -> bool:
    if WHATSAPP_PROVIDER == "cloud_api":
        return await send_whatsapp_cloud_api(phone, message)
    return await send_whatsapp_callmebot(phone, message)

def build_alert_message(student_name: str, subject_name: str, section_name: str, percentage: float) -> str:
    return (
        f"Attendance Alert - HITS\n\n"
        f"Dear {student_name},\n\n"
        f"Your attendance in {subject_name} ({section_name}) "
        f"has dropped to {percentage:.1f}%, which is below the required 75%.\n\n"
        f"Please attend classes regularly to avoid any academic issues.\n\n"
        f"- HITS Attendance Monitoring System"
    )
