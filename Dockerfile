FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /mc_tg_bot

COPY . /mc_tg_bot/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]