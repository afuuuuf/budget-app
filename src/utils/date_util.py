import calendar
from datetime import datetime


class DateUtil:
    @staticmethod
    def get_current_month_name() -> str:
        return calendar.month_name[datetime.now().month]

    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now()
