import time


# this class should be initialized once for every type of request, ex.: google request
class TrafficManager:
    # each request should get a random delay
    _requests_per_second = 10
    _delay_variation = 0.10

    _current_timeout_duration = 0.0
    _timeout_duration_increment = 120
    _timeout_date_start = 0  # unix seconds

    def report_ban(self):
        pass

    def report_no_ban(self):
        pass

    def await_delay(self):
        pass

    def is_ban_active(self):
        pass
