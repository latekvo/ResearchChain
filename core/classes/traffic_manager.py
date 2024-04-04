import random
import time


# this class should be initialized once for every type of request, ex.: google request
class TrafficManager:
    # each request should get a random delay
    _requests_per_second = 10
    _delay_per_request = 0.10  # calculated in constructor
    _delay_variation = 20  # in percent

    _current_timeout_duration = 0.0
    _timeout_duration_increment = 120
    _timeout_date_end = 0.0  # unix seconds

    def report_timeout(self):
        current_date = time.time()
        # timeout duration increases until no timeout is reported
        self._current_timeout_duration += self._timeout_duration_increment
        self._timeout_date_end = current_date + self._current_timeout_duration

    def report_no_timeout(self):
        self._timeout_date_end = 0
        self._current_timeout_duration = 0

    def await_delay(self):
        current_variation = (
            1 - random.randrange(-self._delay_variation, self._delay_variation, 1) / 100
        )
        sleep_duration = self._delay_per_request * current_variation
        time.sleep(sleep_duration)

    def is_timeout_active(self):
        current_date = time.time()
        return self._timeout_date_end > current_date
