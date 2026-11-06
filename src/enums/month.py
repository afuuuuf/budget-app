from enum import StrEnum


class Month(StrEnum):
    JANUARY = "JANUARY"
    FEBRUARY = "FEBRUARY"
    MARCH = "MARCH"
    APRIL = "APRIL"
    MAY = "MAY"
    JUNE = "JUNE"
    JULY = "JULY"
    AUGUST = "AUGUST"
    SEPTEMBER = "SEPTEMBER"
    OCTOBER = "OCTOBER"
    NOVEMBER = "NOVEMBER"
    DECEMBER = "DECEMBER"

    @classmethod
    def _missing_(
        cls, value: object
    ) -> "Month | None":  # lets "november" resolve too
        if isinstance(value, str):
            return cls.__members__.get(value.strip().upper())
        return None

    @property
    def number(self) -> int:
        return list(type(self)).index(self) + 1

    @classmethod
    def from_number(cls, n: int) -> "Month":
        return list(cls)[n - 1]
