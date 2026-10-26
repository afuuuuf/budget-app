import calendar
from datetime import date, datetime
from zoneinfo import ZoneInfo

LOCAL_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


class DateUtil:
    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now(LOCAL_TIMEZONE)

    @staticmethod
    def get_today_date() -> date:
        return DateUtil.get_current_time().date()

    @staticmethod
    def get_current_month_name() -> str:
        return calendar.month_name[DateUtil.get_current_time().month]
