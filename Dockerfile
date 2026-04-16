# Используем официальный образ Python
FROM python:3.12-slim

# Установка системных зависимостей для matplotlib и других библиотек
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем конфигурационные файлы
COPY pyproject.toml README.md ./

# Установка зависимостей проекта
RUN pip install --no-cache-dir .

# Копируем исходный код
COPY . .

# Создаем директории для данных и вывода
RUN mkdir -p output eugenia_data

# Переменная окружения для корректной работы matplotlib в headless режиме
ENV QT_QPA_PLATFORM=offscreen

# Точка входа
ENTRYPOINT ["python", "generate.py"]
