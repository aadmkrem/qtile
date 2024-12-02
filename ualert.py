import subprocess
import time
import logging
import json
import os
from datetime import datetime
from telegram import Bot, TelegramError

# Настройка логирования
logging.basicConfig(
    filename='/var/log/device_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Загрузка конфигурации из файла
config_path = os.getenv('CONFIG_PATH', 'config.json')

try:
    with open(config_path) as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    logging.error('Конфигурационный файл не найден: %s', config_path)
    exit(1)  # Завершение программы с кодом 1 при отсутствии конфигурационного файла
except json.JSONDecodeError:
    logging.error('Ошибка при чтении конфигурационного файла. Убедитесь, что файл имеет корректный формат JSON.')
    exit(1)

TOKEN = os.getenv('TELEGRAM_TOKEN', config['TOKEN'])
CHAT_ID = config['CHAT_ID']
device_hostname = config['device_hostname']
bot = Bot(token=TOKEN)

def is_device_connected(hostname):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', hostname])
        return True
    except subprocess.CalledProcessError:
        return False

last_status = False
logging.info('Сервис запущен и начинает проверку устройства.')
while True:
    try:
        current_status = is_device_connected(device_hostname)

        if current_status and not last_status:
            connection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f'Смартфон подключен к Wi-Fi! Время подключения: {connection_time}'
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                logging.info('Устройство подключено к Wi-Fi. Время подключения: %s', connection_time)
            except TelegramError as e:
                logging.error('Ошибка при отправке сообщения: %s', e)
        elif not current_status and last_status:
            disconnection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f'Смартфон отключен от Wi-Fi! Время отключения: {disconnection_time}'
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                logging.info('Устройство отключено от Wi-Fi. Время отключения: %s', disconnection_time)
            except TelegramError as e:
                logging.error('Ошибка при отправке сообщения: %s', e)

        last_status = current_status
        time.sleep(600)  # Проверяем каждые 10 минут
    except Exception as e:
        logging.error('Произошла ошибка: %s', e)
        time.sleep(60)  # Необходимо подождать перед следующей проверкой
