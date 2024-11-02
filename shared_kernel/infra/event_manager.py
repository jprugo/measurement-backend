import threading
import queue
from shared_kernel.infra import logger

class EventManager:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.subscribers = []
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            if not self.running:
                self.running = True
                threading.Thread(target=self.process_events, daemon=True).start()
                logger.logger.info("EventManager started.")

    def stop(self):
        with self.lock:
            self.running = False
        self.clear_events()
        logger.logger.info("EventManager stopped.")

    def publish(self, message, **kwargs):
        with self.lock:
            if self.running:
                self.event_queue.put((message, kwargs))
                self.notify_subscribers(message, **kwargs)

    def subscribe(self, callback):
        with self.lock:
            self.subscribers.append(callback)

    def notify_subscribers(self, message, **kwargs):
        for callback in self.subscribers:
            callback(message, **kwargs)

    def process_events(self):
        logger.logger.info("Processing events...")
        while self.running:
            try:
                message, kwargs = self.event_queue.get(timeout=0.1)
                self.handle_event(message, **kwargs)
            except queue.Empty:
                continue

    def handle_event(self, message, **kwargs):
        logger.logger.info(f"Processed event: {message} with args: {kwargs}")

    def clear_events(self):
        while not self.event_queue.empty():
            self.event_queue.get()
        logger.logger.info("Cleared all events.")
