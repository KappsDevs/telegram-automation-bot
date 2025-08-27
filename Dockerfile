FROM python:3.12-slim

# install app dependencies
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get install -y libgl1


WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]