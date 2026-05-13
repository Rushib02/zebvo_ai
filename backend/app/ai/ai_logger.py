import logging

class AILogger:
    @staticmethod
    def log_request(model, task, prompt, duration, response):
        print(f"[AI REQUEST] Model: {model}, Task: {task}, Duration: {duration:.2f}s")

    @staticmethod
    def log_error(task, error, model=None):
        print(f"[AI ERROR] Task: {task}, Model: {model}, Error: {error}")
