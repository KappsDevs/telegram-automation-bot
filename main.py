import asyncio
import io
import os
import select
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image
from telethon import TelegramClient
from telethon import events

import connection
import database

COLUMNS = ['message_id', 'sender', 'content', 'date', 'ocr_text']
KEYWORDS = ['R$', 'senha', 'RS', 'pix', 'bicho', 'real', 'reais', 'rapido']
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = TelegramClient('my_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


async def get_ocr_text(message):
    if message.photo:
        try:
            image_bytes = await client.download_media(message, file=bytes)
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            img_cv = np.array(image)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 3)
            gray = cv2.equalizeHist(gray)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            processed_image = Image.fromarray(gray)

            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed_image, config=custom_config)

            return text
        except Exception as e:
            print(f"Error getting image string: {e}")

    return None



@client.on(events.NewMessage())
async def get_messages(event):
    text = ""
    message = event.message
    try:
        if message.photo:
            text = await get_ocr_text(message)

        if any(keyword.lower() in message.text.lower() for keyword in KEYWORDS) or any(
                keyword.lower() in text.lower()for keyword in KEYWORDS):
            database.insert_into_db(message, text)

    except Exception as e:
        print(f"Error getting new message: {e}")


def send_mail(messages):
    output = io.BytesIO()
    pd.DataFrame(messages, columns=COLUMNS).to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    message_ids = [m['message_id'] for m in messages]

    msg = MIMEMultipart()
    msg["From"] = os.getenv("MAIL")
    msg["To"] = os.getenv("MAIL")
    msg["Subject"] = 'Fraud Alert'

    body = f"""
        Hello,
        
        The system has detected 5 suspected fraud messages in the monitored Telegram groups.
        
        Please see the attached Excel file for the full details of the suspicious messages.
        
        Best regards,
        Fraud Monitoring Bot 
    """

    msg.attach(MIMEText(body, "plain"))

    attachment = MIMEApplication(output.getvalue(), _subtype="xlsx")
    attachment.add_header("Content-Disposition", "attachment", filename="Alerts.xlsx")

    msg.attach(attachment)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("MAIL"), os.getenv("PASSWORD"))
            server.send_message(msg)
    except Exception as e:
        print(f'Error sending email: {e}')
    else:
        database.mark_messages_as_sent(message_ids)
        print("Email sent successfully")



async def check_unsent_messages_periodically():
    while True:
        messages = database.get_unsent_messages()
        if len(messages) >= 5:
            await asyncio.to_thread(send_mail, messages)
        await asyncio.sleep(5)



async def main():
    # database.truncate_table()
    database.create_messages_table()

    asyncio.create_task(check_unsent_messages_periodically())

    await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
