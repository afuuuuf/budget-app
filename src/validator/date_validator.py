from datetime import date

from ..utils import DateUtil


class DateValidator:
    @staticmethod
    def futureDateValidation(dateValue: date) -> date:
        if dateValue <= DateUtil.get_today_date():
            raise ValueError("must be a future date")
        return dateValue

    @staticmethod
    def dateIsoFormatValidation(dateValue: date | str) -> date:
        if isinstance(dateValue, str):
            try:
                return date.fromisoformat(dateValue.strip())
            except ValueError:
                raise ValueError(
                    'must be in "YYYY-MM-DD" format (e.g. 2026-11-25'
                ) from None
        return dateValue

    @staticmethod
    def notFutureDateValidation(dateValue: date) -> date:
        if dateValue > DateUtil.get_today_date():
            raise ValueError("cannot be in the future")
        return dateValue
