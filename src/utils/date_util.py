from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

from ..enums import Month

LOCAL_TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


@dataclass(frozen=True)
class DateRange:
    start: date  # inclusive
    end: date  # exclusive

    @classmethod
    def of_month(cls, year: int, month: Month) -> "DateRange":
        m = month.number
        start = date(year, m, 1)
        end = date(year + 1, 1, 1) if m == 12 else date(year, m + 1, 1)
        return cls(start, end)


class DateUtil:
    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now(LOCAL_TIMEZONE)

    @staticmethod
    def get_today_date() -> date:
        return DateUtil.get_current_time().date()

    @staticmethod
    def get_current_month() -> Month:
        return Month.from_number(DateUtil.get_current_time().month)

    @staticmethod
    def get_current_year() -> int:
        return DateUtil.get_current_time().year
