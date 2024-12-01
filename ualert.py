import subprocess
import time
import logging
from telegram import Bot

# Настройка логирования
logging.basicConfig(
    filename='/var/log/device_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TOKEN = ''
CHAT_ID = ''
bot = Bot(token=TOKEN)

def is_device_connected(hostname):
    try:
        output = subprocess.check_output(['ping', '-c', '1', hostname])
        return True
    except subprocess.CalledProcessError:
        return False

device_hostname = ''
last_status = False

logging.info('Сервис запущен и начинает проверку устройства.')
while True:
    try:
        current_status = is_device_connected(device_hostname)

        if current_status and not last_status:
            bot.send_message(chat_id=CHAT_ID, text='Смартфон подключен к Wi-Fi!')
            logging.info('Устройство подключено к Wi-Fi.')
        elif not current_status and last_status:
            bot.send_message(chat_id=CHAT_ID, text='Смартфон отключен от Wi-Fi!')
            logging.info('Устройство отключено от Wi-Fi.')

        last_status = current_status
        time.sleep(600)  # Проверяем каждые 10 минут
    except Exception as e:
        logging.error('Произошла ошибка: %s', e)
        time.sleep(60)  # Необходимо подождать перед следующей проверкой
