import queue
from concurrent.futures import ThreadPoolExecutor



class BoundedThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers,thread_name_prefix)
        # self._work_queue = queue.Queue(max_workers * 2)
        self._work_queue = queue.Queue(100)