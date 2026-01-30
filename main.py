import os
import requests
import time
from datetime import datetime, timezone
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_URL = "https://imageriegap.mon-portail-patient.net/api/pp/availabilities/locations?idAct=2109020959&idLocation=11157572092"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8556080794")
CHECK_INTERVAL = 15 * 60  # 15 minutes in seconds
LIMIT_DATE = datetime(2026, 2, 4, tzinfo=timezone.utc)


def send_telegram_message(message):
    """Send a message via Telegram bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set!")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Telegram notification sent successfully")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


def check_availability():
    """Check appointment availability and notify if condition is met."""
    try:
        logger.info(f"Checking availability at {API_URL}")
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Received data: {data}")
        
        # Check if data is an array with at least one element containing firstSchedule
        if isinstance(data, list) and len(data) > 0 and data[0].get("firstSchedule"):
            first_schedule = data[0]["firstSchedule"]
            first_date = datetime.fromisoformat(first_schedule.replace("Z", "+00:00"))
            
            logger.info(f"First available schedule: {first_date.strftime('%Y-%m-%d %H:%M')}")
            logger.info(f"Limit date: {LIMIT_DATE.strftime('%Y-%m-%d')}")
            
            if first_date < LIMIT_DATE:
                # Format the message
                date_str = first_date.strftime("%d/%m/%Y")
                time_str = first_date.strftime("%H:%M")
                message = f"🏥 <b>Nouveau RDV dispo!</b>\n\n📅 Date: {date_str}\n🕐 Heure: {time_str}"
                
                logger.info("Condition met! Sending notification...")
                send_telegram_message(message)
            else:
                logger.info("First available date is after the limit date")
        else:
            logger.info("No available schedules found")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching availability data: {e}")
    except (ValueError, KeyError, IndexError) as e:
        logger.error(f"Error parsing response data: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


def main():
    """Main loop to check availability every 15 minutes."""
    logger.info("Starting appointment availability monitor...")
    logger.info(f"Checking every {CHECK_INTERVAL // 60} minutes")
    logger.info(f"Limit date: {LIMIT_DATE.strftime('%Y-%m-%d')}")
    
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set. Notifications will fail!")
    
    # Initial check
    check_availability()
    
    # Continuous monitoring
    while True:
        time.sleep(CHECK_INTERVAL)
        check_availability()


if __name__ == "__main__":
    main()
