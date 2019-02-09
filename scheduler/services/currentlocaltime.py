from datetime import datetime
import calendar


class CurrentLocalTime:
    def __init__(self):
        self.today = None
        self._hour = None
        self._minute = None
        self.now()

    def find_day(self):
        # IPython.embed()
        day_number = datetime.strptime(self.today, '%Y %m %d').weekday()
        return calendar.day_name[day_number].lower()

    def now(self):
        self.today = datetime.now().strftime('%Y %m %d')
        self._hour, self._minute = datetime.now().strftime('%H:%M').split(':')

    def day(self):
        return self.find_day()

    def hour(self):
        return self._hour

    def minute(self):
        return self._minute