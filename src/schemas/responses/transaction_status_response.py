from pydantic import BaseModel

from ...enums import Status


class TransactionStatusResponse(BaseModel):
    status: str

    @classmethod
    def get_status_message(cls, message: Status) -> "TransactionStatusResponse":
        return cls(status=message.value)
