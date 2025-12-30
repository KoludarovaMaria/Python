import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Создайте файл .env с BOT_TOKEN=ваш_токен
