MAX_AMOUNT = 10**12


class AmountValidator:
    @staticmethod
    def non_zero(amountValue: int) -> int:
        if 0 == amountValue:
            raise ValueError("cannot be 0")
        return amountValue

    @staticmethod
    def within_limit(amountValue: int) -> int:
        if abs(amountValue) > MAX_AMOUNT:
            raise ValueError(f"must not exceed {MAX_AMOUNT} in absolute value")
        return amountValue
