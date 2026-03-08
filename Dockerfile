# Используем официальный базовый образ Playwright с Python.
# Он уже включает в себя все необходимые системные зависимости и браузеры.
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения в рабочую директорию
COPY . .

# Команда для запуска бота при старте контейнера
CMD ["python", "main.py"]