FROM python:3.11-slim

WORKDIR /mc_tg_bot

COPY . /mc_tg_bot/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
