import os
import threading
import time

import psutil


class PeakMemoryMonitor:
    """
    Monitor the peak RSS memory usage of the current process.
    """

    def __init__(self, interval: float = 0.01):
        self.interval = interval
        self.process = psutil.Process(os.getpid())

        self.peak_memory = 0

        self._running = False
        self._thread = None

    def _monitor(self):
        while self._running:
            memory = self.process.memory_info().rss

            if memory > self.peak_memory:
                self.peak_memory = memory

            time.sleep(self.interval)

    def start(self):
        self.peak_memory = self.process.memory_info().rss

        self._running = True

        self._thread = threading.Thread(
            target=self._monitor,
            daemon=True,
        )

        self._thread.start()

    def stop(self):
        self._running = False

        if self._thread is not None:
            self._thread.join()

        # Final measurement
        memory = self.process.memory_info().rss

        if memory > self.peak_memory:
            self.peak_memory = memory

    @property
    def peak_memory_mb(self):
        return self.peak_memory / (1024 ** 2)