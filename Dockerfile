FROM python:3.11-slim

# Установите необходимые пакеты для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    pkg-config \
    libffi-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установите Rust и Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Добавьте Rust в PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Обновите pip до последней версии
RUN pip install --upgrade pip

# Установите зависимости
WORKDIR /mc_tg_bot
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Копируйте остальной код
COPY . .

CMD ["python", "main.py"]
