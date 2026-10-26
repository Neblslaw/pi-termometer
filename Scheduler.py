import time
import threading
from typing import Callable


class Scheduler:
    def __init__(self, interval: float, task: Callable):
        """
        :param interval: Time in seconds between task executions.
        :param task: The function or method to execute.
        """
        self.interval = interval
        self.task = task
        self._running = False
        self._thread = None

    def start(self):
        """Starts the background scheduling thread."""
        if self._running:
            return  # Already running

        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stops the scheduler and waits for the thread to finish."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join()

    def _run(self):
        """Internal drift-free loop."""
        next_call = time.monotonic()

        while self._running:
            # Execute the target function
            self.task()

            # Calculate the exact time for the next execution
            next_call += self.interval
            sleep_duration = next_call - time.monotonic()

            # Sleep only for the remaining time
            if sleep_duration > 0:
                time.sleep(sleep_duration)