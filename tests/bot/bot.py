import logging
from queue import Queue
from threading import Lock, Thread, current_thread

from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import Dispatcher, run_async

from spockesman import process

log = logging.getLogger(__name__)
message_queue = Queue()


class TelegramBot:
    __updater: Updater
    __dispatcher: Dispatcher
    __number_threads = 4

    def __init__(self):
        self.__locks = {}
        self.__images = {}
        for _ in range(TelegramBot.__number_threads):
            t = Thread(target=self.process_messages, daemon=True)
            t.start()
        self.create_bot()

    def create_bot(self):
        self.__updater = Updater(token='653570948:AAHY7epbKTYsO5ajIlLR3kBMZZ-6LNLnFr0')
        self.__dispatcher = self.__updater.dispatcher
        self.__dispatcher.add_handler(MessageHandler(Filters.all, self.text_handler))
        self.__dispatcher.add_handler(CallbackQueryHandler(self.inline_handler))

    def get_lock(self, chat_id):
        if chat_id not in self.__locks:
            self.__locks[chat_id] = Lock()
        return self.__locks[chat_id].acquire(False)

    def release_lock(self, chat_id):
        self.__locks[chat_id].release()
        self.__locks.pop(chat_id)

    def get_bot_info(self):
        return self.__updater.bot.get_me()

    @property
    def start_method(self):
        return self.__updater.start_polling

    @run_async
    def text_handler(self, bot, update):
        log.info(f"[BOT] Received message '{update.message.text}' from '{update.message.chat_id}'")
        self.main_handler(bot, update.message.text, update.message.chat_id, update)

    @run_async
    def inline_handler(self, bot, update):
        log.info(f"[BOT] Received callback '{update.callback_query.data}'"
                 f" from '{update.callback_query.message.chat_id}'")
        self.main_handler(bot, update.callback_query.data, update.callback_query.message.chat_id, update)

    def main_handler(self, bot, text, chat_id, update):
        # prevent spam
        if not self.get_lock(chat_id):
            return
        try:
            log.info(f"[BOT] Processing input '{text}' from '{chat_id}'")
            reply, ui = process(chat_id, text)
            if reply or ui:
                message_queue.put((chat_id, reply, ui))
        except Exception as e:
            log.exception(e)
        finally:
            log.info(f"[BOT] Exiting main handler for '{chat_id}'")
            self.release_lock(chat_id)

    def process_messages(self):
        while True:
            log.info(f"[MSG_THREAD {current_thread().ident}] Getting next message")
            chat_id, text, ui = message_queue.get()
            try:
                self.__updater.bot.send_message(chat_id=chat_id, text=text, reply_markup=ui)
            except Exception as e:
                log.exception(e)
            log.info(f"[MSG_THREAD {current_thread().ident}] Message for '{chat_id}' finished")
            message_queue.task_done()


bot = TelegramBot()
