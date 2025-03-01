import win32com.client
import json
import pywintypes  # Required for date conversion
import logging
from datetime import datetime

# Configure logging
log_filename = "main.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    # Load data from main.json
    with open("main.json", "r") as file:
        data = json.load(file)

    subject = data["subject"]
    attendees = data.get("required_attendees", [])  # Handle missing attendees gracefully

    # Get today's date and convert it to pywintypes datetime
    today = datetime.today()
    today_pytime = pywintypes.Time(today)  # Convert to pywintypes.datetime

    # Connect to Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    logging.info("Connected to Outlook.")

    # Create an all-day event
    appointment = outlook.CreateItem(1)  # 1 = Appointment Item
    appointment.Subject = subject
    appointment.Start = today_pytime  # Correct format
    appointment.AllDayEvent = True
    appointment.BusyStatus = 0  # 0 = Free (1 = Tentative, 2 = Busy, 3 = OOO)
    appointment.MeetingStatus = 1  # Convert to a meeting request

    logging.info(f"Created Out of Office event: {subject}")

    # Add required attendees
    for attendee in attendees:
        recipient = appointment.Recipients.Add(attendee)
        recipient.Type = 1  # 1 = Required Attendee
        logging.info(f"Added attendee: {attendee}")

    # Send the meeting invite
    if attendees:
        appointment.Send()
        logging.info(f"Sent OOO invite to: {', '.join(attendees)}")
    else:
        appointment.Save()  # Just save the event if no attendees
        logging.info("Saved OOO event (No attendees).")

except Exception as e:
    logging.error(f"Error: {str(e)}", exc_info=True)
