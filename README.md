# Telegram Automation Bot 🤖

A **Python-based bot** for automating message handling on **Telegram**.  
Its main goal is to capture messages (text and images) and store them in a database for further analysis.

---

## 🚀 Features
- Capture incoming messages from Telegram (text and images).  
- Extract text from images using **OCR**.  
- Store messages in a **PostgreSQL** database.  
- Real-time listener for monitoring unsent messages.  
- Run locally or via **Docker Compose**.  

---

## 🛠️ Technologies
- Python 3.10+
- [Telethon](https://docs.telethon.dev/) (Telegram API client)  
- [Pillow](https://pillow.readthedocs.io/) & [OpenCV](https://opencv.org/) (image processing)  
- [Pytesseract](https://pypi.org/project/pytesseract/) (OCR)  
- [PostgreSQL](https://www.postgresql.org/)  
- [Docker Compose](https://docs.docker.com/compose/)  

---

## 🐳 Running with Docker

### Build and start containers
This will start both the **PostgreSQL database** and the **bot**:
```bash
docker-compose build
docker-compose up
```

## ▶️ Running Locally (without Docker)

Make sure you have **PostgreSQL** running and configured with the same credentials from your `.env` file.

### Start the bot
```bash

python main.py
``` 

## 📡 How the Bot Works

The bot continuously listens for incoming messages on Telegram. Its main workflow is:

1. **Message Filtering:** The bot checks if the message contains specific keywords or criteria that you want to monitor.  
2. **Text Extraction:** If the message includes an image, the bot performs **OCR** to extract text from the image.  
3. **Data Storage:** Both the message text and the OCR results are stored in a **PostgreSQL** database.
4. **Event Triggering:** When certain conditions are met (e.g., a message matches specific keywords or the number of unsent messages exceeds a threshold), the bot automatically sends an **email notification** to alert the user. 





