from queue import Queue


message_queue = Queue()


def send_message(chat_id, message):
    if not message:
        return
    message_queue.put((chat_id, message))


def send_messages(chat_ids, message=None):
    if not message:
        return
    for chat_id in chat_ids:
        send_message(chat_id, message)
