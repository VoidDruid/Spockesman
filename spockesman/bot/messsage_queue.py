from queue import Queue


# TODO: implement caching messages to redis backend if queue becomes too long
class OrderedKeyQueue(Queue):
    """
    Queue that orders items put into it by thier keys.
    If there is already an item with the same key in queue, next item will be placed in 'waiting list',
    and put in queue after previous item was processed.

    NOTE: intended to be used with messages as items and user ids as keys
    """

    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self._reserve = {}

    def put_item(self, key, item, block=True, timeout=None):
        super().put((key, item), block=block, timeout=timeout)

    def add(self, key, item, block=True, timeout=None):
        with self.mutex:
            if key not in self._reserve:
                self._reserve[key] = []
            else:
                self._reserve[key].append(item)
                return
        self.put_item(key, item, block, timeout)

    def task_completed(self, key):
        if key not in self._reserve:
            super().task_done()
            return
        with self.mutex:
            next_item = None
            if self._reserve[key]:
                next_item = self._reserve[key].pop(0)
            if not self._reserve[key]:
                self._reserve.pop(key)
        if next_item:
            self.put_item(key, next_item)
        super().task_done()
