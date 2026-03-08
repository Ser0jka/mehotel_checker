# Используем стабильный образ Playwright
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# Устанавливаем рабочую директорию
WORKDIR /app

# Отключаем создание .pyc файлов и включаем небуферизованный вывод логов
# (чтобы вы сразу видели сообщения в docker logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Явно устанавливаем только нужный браузер (экономит место)
RUN playwright install chromium

# Копируем код
COPY . .

# Запуск
CMD ["python", "main.py"]