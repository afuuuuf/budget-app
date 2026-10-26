from pydantic import BaseModel

from ...enums import Status


class StatusResponse(BaseModel):
    status: str

    @classmethod
    def get_status_message(cls, message: Status) -> "StatusResponse":
        return cls(status=message.value)
