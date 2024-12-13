import logging
from telegram.ext import ApplicationBuilder, Defaults
from dotenv import load_dotenv
import os
from handlers import setup_handlers
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import signal
import time
import pytz

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class BotRestartHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".log"):
            os.kill(os.getpid(), signal.SIGINT)

def start_bot_with_restart():
    event_handler = BotRestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    while True:
        try:
            main()
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            logger.info("Restarting the bot in 5 seconds...")
            time.sleep(5)
        finally:
            observer.stop()
            observer.join()

def main() -> None:
    tz = pytz.timezone(os.getenv('TZ', 'UTC'))
    defaults = Defaults(tzinfo=tz)
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).defaults(defaults).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == '__main__':
    start_bot_with_restart()
