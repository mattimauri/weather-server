import time

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def allow_request(self):
        now = time.time()
        # Rimuovi le chiamate più vecchie del periodo
        self.calls = [call for call in self.calls if now - call <= self.period]
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False