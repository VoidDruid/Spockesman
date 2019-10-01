import logging
from queue import Queue
from threading import Lock, Thread, current_thread

from telegram.ext import Filters, MessageHandler, Updater
from telegram.ext.dispatcher import Dispatcher, run_async

from spockesman import process

from .token import TOKEN  # provide your own telegram token

log = logging.getLogger(__name__)
message_queue = Queue()


class TelegramBot:
    _updater: Updater
    _dispatcher: Dispatcher
    _number_threads = 4

    def __init__(self):
        self._locks = {}
        for _ in range(TelegramBot._number_threads):
            t = Thread(target=self.process_messages, daemon=True)
            t.start()
        self.create_bot()

    def create_bot(self):
        self._updater = Updater(token=TOKEN)
        self._dispatcher = self._updater.dispatcher
        self._dispatcher.add_handler(MessageHandler(Filters.all, self.text_handler))

    def get_lock(self, chat_id):
        if chat_id not in self._locks:
            self._locks[chat_id] = Lock()
        return self._locks[chat_id].acquire(False)

    def release_lock(self, chat_id):
        self._locks[chat_id].release()
        self._locks.pop(chat_id)

    @property
    def start_method(self):
        return self._updater.start_polling

    @run_async
    def text_handler(self, bot, update):
        log.info(f"[BOT] Received message '{update.message.text}' from '{update.message.chat_id}'")
        self.main_handler(update.message.text, update.message.chat_id)

    def main_handler(self, text, chat_id):
        # prevent spam
        if not self.get_lock(chat_id):
            return
        try:
            log.info(f"[BOT] Processing input '{text}' from '{chat_id}'")
            reply = process(chat_id, text)
            if reply:
                message_queue.put((chat_id, reply))
        except Exception as e:
            log.exception(e)
        finally:
            log.info(f"[BOT] Exiting main handler for '{chat_id}'")
            self.release_lock(chat_id)

    def process_messages(self):
        while True:
            log.info(f"[MSG_THREAD {current_thread().ident}] Getting next message")
            chat_id, reply = message_queue.get()
            try:
                self._updater.bot.send_message(chat_id=chat_id, text=reply.text, reply_markup=reply.ui)
            except Exception:
                log.exception(
                    f"[MSG_THREAD {current_thread().ident}] "
                    f"Error while sending message for '{chat_id}'"
                )
            else:
                log.info(f"[MSG_THREAD {current_thread().ident}] Message for '{chat_id}' finished")
            message_queue.task_done()


bot = TelegramBot()
